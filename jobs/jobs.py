# import itertools
import json
import os
import random
# import sys
import time
import requests
from datetime import datetime, timedelta
from apscheduler.jobstores.base import JobLookupError
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from pytz import utc

load_dotenv()

from utils import dataBases

mongoDataBase = dataBases.mongodb_client


def scheduled_start_voting():
    from jobs.updater import sched
    # print('Scheduled Start Voting Running')
    try:
        if not mongoDataBase.check_connection():
            start_vote = datetime.now(tz=utc) + timedelta(hours=1)
            start_vote = start_vote.strftime('%Y-%m-%d %H:%M:%S')

            sched.get_job('scheduled_start_voting').modify(next_run_time=start_vote)
            return

        query = {'_id': 0, 'candidates': 1, 'chat': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return

        if (
                'president' not in document.get('candidates', {}).values() or
                'parliament' not in document.get('candidates', {}).values()
        ):
            # Not start vote without candidates

            start_vote = datetime.now(tz=utc) + relativedelta(months=3)
            start_vote = start_vote.strftime('%Y-%m-%d 00:00:00')

            query = {'start_vote': f'{start_vote}'}

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                       action='$set', query=query)

            text = f"**Недостаточно кандидатов на выборы [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech | Выборы были перенесены**"

            chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
            origin = os.getenv('HOSTNAME', '')

            data = {
                "text": text,
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            }

            data = json.dumps(data)

            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat_username}", data=data,
                          headers={'Origin': origin, 'Host': origin})

            return

        end_vote = datetime.now(tz=utc) + timedelta(days=1)
        end_vote = end_vote.strftime('%Y-%m-%d %H:%M:%S')

        start_vote = datetime.now(tz=utc) + relativedelta(months=3)
        start_vote = start_vote.strftime('%Y-%m-%d 00:00:00')

        query = {'end_vote': f'{end_vote}', 'start_vote': f'{start_vote}'}

        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                   action='$set', query=query)

        sched.add_job(scheduled_end_voting, 'date', run_date=end_vote)
        sched.add_job(scheduled_start_voting, 'date', run_date=start_vote)

        text = f"**В данный момент на [официальном сайте]({os.getenv('HOSTNAME', '')}freedom_of_speech) проходят [выборы Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech**"

        chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
        origin = os.getenv('HOSTNAME', '')

        data = {
            "text": text,
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }

        data = json.dumps(data)

        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat_username}", data=data,
                      headers={'Origin': origin, 'Host': origin})
    except Exception as e:
        print(e)

    sched.print_jobs()

def scheduled_end_voting():
    from jobs.updater import sched
    # print('Scheduled End Voting Running')
    try:
        if not mongoDataBase.check_connection():
            end_vote = datetime.now(tz=utc) + timedelta(hours=1)
            end_vote = end_vote.strftime('%Y-%m-%d %H:%M:%S')

            sched.get_job('scheduled_end_voting').modify(next_run_time=end_vote)

            sched.print_jobs()

            return

        query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'start_vote': 1, 'end_vote': 1,
                 'votes': 1, 'candidates': 1, 'chat': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return

        # Find the most votes candidates (president, parliament)
        votes = document.get('votes', {})

        if votes:
            president_votes = votes.get('president', {})
            parliament_votes = votes.get('parliament', {})
            candidates = document.get('candidates', {})

            if president_votes:
                # Count votes for candidate
                count_votes = {v: list(president_votes.values()).count(v) for v in set(president_votes.values())}
                # Sort result
                sorted_count_votes = sorted(count_votes.items())
                # Same amount of votes
                winners_count = list(count_votes.values()).count(max(count_votes.values()))
                # List of candidates that have same amount of votes
                list_of_maxes = sorted_count_votes[0:winners_count]
                # Random candidate winner from same amount of votes or just max votes winner
                president = random.sample(list_of_maxes, 1)[0][0]
            else:
                # No president votes
                if candidates:
                    # List of president candidates
                    president_candidates = [candidate for candidate, role in candidates.items() if role == 'president']
                    # Random candidate winner from all candidates for president
                    president = random.sample(president_candidates, 1)[0]
                else:
                    # No candidates at all for president
                    president = document.get('president', '')

            if parliament_votes:
                count_votes = {v: list(parliament_votes.values()).count(v) for v in set(parliament_votes.values())}
                sorted_count_votes = sorted(count_votes.items())
                winners_count = list(count_votes.values()).count(max(count_votes.values()))
                list_of_maxes = sorted_count_votes[0:winners_count]
                parliament = random.sample(list_of_maxes, 1)[0][0]
            else:
                # No president votes
                if candidates:
                    # List of president candidates
                    parliament_candidates = [candidate for candidate, role in candidates.items() if
                                             role == 'parliament']
                    # Random candidate winner from all candidates for president
                    parliament = random.sample(parliament_candidates, 1)[0]
                else:
                    # No candidates at all for parliament
                    parliament = document.get('parliament', '')
        else:
            president = document.get('president', '')
            parliament = document.get('parliament', '')

        chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
        origin = os.getenv('HOSTNAME', '')

        judge = document.get('judge', {}).get('judge', '')
        if president == judge or parliament == judge:
            query = {'judge.judge': ''}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                       action='$unset', query=query)

        if president != document.get('president', ''):
            # Demote old president
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'demote_chat_member',
            }
            data = json.dumps(data)
            old_president = document.get('president', '')
            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{old_president}",
                          data=data, headers={'Origin': origin, 'Host': origin})
            # Promote new president
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'promote_chat_member',
                'parameters': {'custom_title': 'Президент'},
            }
            data = json.dumps(data)
            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{president}",
                          data=data, headers={'Origin': origin, 'Host': origin})

        if parliament != document.get('parliament', ''):
            # Demote old parliament
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'demote_chat_member',
            }
            data = json.dumps(data)
            old_parliament = document.get('parliament', '')
            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{old_parliament}",
                          data=data, headers={'Origin': origin, 'Host': origin})
            # Promote new parliament
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'promote_chat_member',
                'parameters': {'custom_title': 'Парламент'},
            }
            data = json.dumps(data)

            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{parliament}",
                          data=data, headers={'Origin': origin, 'Host': origin})

        # Delete vote and votes information from database
        query = {'end_vote': '', 'votes': '', 'candidates': '', 'referendum.votes': ''}
        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                   action='$unset', query=query)

        # Set new president, parliament in database
        query = {"parliament": parliament, 'president': president}
        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                   action='$set', query=query)

        users = document.get('users', {})
        tpresident = users.get(president, {}).get('telegram', {}).get('username', '')
        tparliament = users.get(parliament, {}).get('telegram', {}).get('username', '')

        text = f"**Завершены выборы [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech:\n\n**"
        if tpresident:
            text = f"{text}Новый Президент: [{president}](t.me/{tpresident})\n"
        else:
            text = f"{text}Новый Президент: {president}\n"

        if tparliament:
            text = f"{text}Новый Парламент: [{parliament}](t.me/{tparliament})\n"
        else:
            text = f"{text}Новый Парламент: {parliament}\n"

        data = {
            "text": text,
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }

        data = json.dumps(data)

        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat_username}", data=data,
                      headers={'Origin': origin, 'Host': origin})

        referendum_date = datetime.now(tz=utc)
        referendum_date = referendum_date.strftime('%Y-%m-%d %H:%M:%S')
        # Set new referendum be valid only after 30 days after vote
        query = {"referendum.date": referendum_date}
        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                   query=query)
    except Exception as e:
        print(e)


def scheduled_telegram_synching(start=0, stop=200, step=1):
    from jobs.updater import sched

    # sync_time = datetime.now(tz=utc) + timedelta(hours=4)
    # sync_time = sync_time.strftime('%Y-%m-%d %H:%M:%S')

    # sched.add_job(scheduled_telegram_synching, 'date', run_date=sync_time, id='scheduled_telegram_synching')
    # print('Scheduled Telegram Synching Running')
    try:
        if not mongoDataBase.check_connection():
            return

        query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'referendum': 1, 'chat': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return

        last_update = document.get('chat', {}).get('date', '')

        if last_update:
            last_update_seconds = (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update,
                                                                                                 '%Y-%m-%d %H:%M:%S')).seconds
        else:
            last_update_seconds = 14400

        # update only every 4 hours
        if last_update_seconds >= 14400:
            chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            }
            data = json.dumps(data)
            origin = os.getenv('HOSTNAME', '')
            chat = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/chat/{chat_username}", data=data,
                                headers={'Origin': origin, 'Host': origin})

            if chat and chat.status_code == 200:
                chat = chat.json()

                date = datetime.now(tz=utc)
                date = date.strftime('%Y-%m-%d %H:%M:%S')

                query = {'chat.chat_parameters': chat.get('chat_parameters', {}), 'chat.date': date}
                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                           action='$set', query=query)

                # Check for referendum
                referendum_date = document.get('referendum', {}).get('date', '')

                if referendum_date:
                    # timedelta in referendum must be more than 30 days
                    if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(referendum_date,
                                                                                      '%Y-%m-%d %H:%M:%S')).days >= 30:
                        president = document.get('president', '')
                        parliament = document.get('parliament', '')
                        judge = document.get('judge', {}).get('judge', '')

                        # Count of government now
                        government = []

                        if president:
                            government.append(president)
                        if parliament:
                            government.append(parliament)
                        if judge:
                            government.append(judge)

                        referendum_usernames = [username for username, opinion in
                                                document.get('referendum', {}).get('votes', {}).items() if
                                                opinion and username not in government]

                        members_count = chat.get('chat_parameters', {}).get('members_count', '')

                        if members_count:
                            # Count of referendum_true values
                            if (100 * float(len(referendum_usernames)) / float(members_count - len(government))) >= 75:

                                try:
                                    sched.remove_job('scheduled_start_voting')
                                except JobLookupError:
                                    # job not found
                                    pass

                                sched.add_job(scheduled_start_voting, 'date', run_date=datetime.now(tz=utc),
                                              id='scheduled_start_voting')

                                referendum_date = datetime.now(tz=utc)
                                referendum_date = referendum_date.strftime('%Y-%m-%d %H:%M:%S')

                                query = {'referendum.votes': '', 'referendum.date': referendum_date}
                                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                           action='$set', query=query)

            time.sleep(60)

        users = document.get('users', '')

        # Sync data for start, stop, step inverval (60 seconds delay) (default 200 users)
        # for user in itertools.islice(users, start, stop, step):
        # sync_count = 0
        for user in users:
            tuser = users.get(user, '')
            # print(tuser)

            # password = user.get('password', '')
            # sessionid = user.get('sessionid', '')
            # permissions = user.get('permissions', {})

            last_update = tuser.get('date', '')

            if last_update:
                last_update_seconds = (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update,
                                                                                                     '%Y-%m-%d %H:%M:%S')).seconds
            else:
                last_update_seconds = 14400

            # update only every 4 hours
            if last_update_seconds >= 14400:
                telegram = tuser.get('telegram', {})

                if telegram:
                    chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                    telegram_username = telegram.get('username', '')

                    data = {
                        'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                    }
                    data = json.dumps(data)
                    origin = os.getenv('HOSTNAME', '')

                    member = requests.get(
                        f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat_username}/{telegram_username}",
                        data=data, headers={'Origin': origin, 'Host': origin})
                    # sync_count += 1

                    if member and member.status_code == 200:
                        member = member.json()

                        date = datetime.now(tz=utc)
                        date = date.strftime('%Y-%m-%d %H:%M:%S')

                        query = {f'users.{user}.member': member, f'users.{user}.date': date}
                        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                   action='$set', query=query)
                    else:
                        if member.status_code == 422:
                            # if not member or not user or not chat:
                            #     return Response(status=422)

                            # date = datetime.now(tz=utc)
                            # date = date.strftime('%Y-%m-%d %H:%M:%S')

                            if tuser.get('member', ''):
                                query = {f'users.{user}.member': '', f'users.{user}.date': '',
                                         f'referendum.votes.{user}': ''}

                                president = document.get('president', '')
                                parliament = document.get('parliament', '')
                                judge = document.get('judge', {}).get('judge', '')

                                # Unset president, parliament, judge in DataBase
                                if user == president:
                                    query['president'] = ''
                                else:
                                    if user == parliament:
                                        query['parliament'] = ''
                                    else:
                                        if user == judge:
                                            query['judge'] = ''

                                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                           action='$unset', query=query)

                    time.sleep(60)


    except Exception as e:
        print(e)

    sched.print_jobs()


def scheduled_voting():
    from jobs.updater import sched

    try:
        if not mongoDataBase.check_connection():
            date = datetime.now(tz=utc) + timedelta(minutes=15)
            date = date.strftime('%Y-%m-%d %H:%M:%S')

            sched.get_job('scheduled_voting').modify(next_run_time=date)
        else:
            query = {'_id': 0, 'start_vote': 1, 'end_vote': 1}
            document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

            # Start vote job (on start_vote date in db)
            start_vote = document.get('start_vote', '')
            end_vote = document.get('end_vote', '')

            if start_vote:
                sched.add_job(scheduled_start_voting, 'date', run_date=start_vote, id='scheduled_start_voting',
                              misfire_grace_time=None, coalesce=True)

            # End vote job (on end_vote date in db)
            if end_vote:
                sched.add_job(scheduled_end_voting, 'date', run_date=end_vote, id='scheduled_end_voting',
                              misfire_grace_time=None, coalesce=True)
    except Exception as e:
        print(e)

    sched.print_jobs()
