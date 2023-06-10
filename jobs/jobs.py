import itertools
import json
import os
import random
import sys
import time
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from pytz import utc

load_dotenv()

from utils import mongoDataBase

def scheduled_start_voting():
    from .updater import sched
    # print('Scheduled Start Voting Running')
    try:
        query = {'_id': 0, 'candidates': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if 'president' not in document.get('candidates', {}) or 'parliament' not in document.get('candidates', {}):
            # Not start vote without candidates

            start_vote = datetime.now(tz=utc) + relativedelta(months=3)
            start_vote = start_vote.strftime('%Y-%m-%d 00:00:00')

            query = {'start_vote': f'{start_vote}'}

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                       action='$set', query=query)

            text = f"**Недостаточно кандидатов на выборы [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech | Выборы были перенесены**"

            chat = 'freed0m0fspeech'
            origin = os.getenv('HOSTNAME', '')

            data = {
                "text": text,
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            }

            data = json.dumps(data)

            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat}", data=data,
                          headers={'Origin': origin})

            return

        end_vote = datetime.now(tz=utc) + timedelta(days=1)
        end_vote = end_vote.strftime('%Y-%m-%d 00:00:00')

        start_vote = datetime.now(tz=utc) + relativedelta(months=3)
        start_vote = start_vote.strftime('%Y-%m-%d 00:00:00')

        query = {'end_vote': f'{end_vote}', 'start_vote': f'{start_vote}'}

        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                   action='$set', query=query)

        sched.add_job(scheduled_end_voting, 'date', run_date=end_vote)
        sched.add_job(scheduled_start_voting, 'date', run_date=start_vote)

        sched.print_jobs()

        text = f"**В данный момент на [официальном сайте]({os.getenv('HOSTNAME', '')}freedom_of_speech) проходят [выборы Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech**"

        chat = 'freed0m0fspeech'
        origin = os.getenv('HOSTNAME', '')

        data = {
            "text": text,
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }

        data = json.dumps(data)

        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat}", data=data,
                      headers={'Origin': origin})
    except:
        pass


def scheduled_end_voting():
    # print('Scheduled End Voting Running')
    try:
        query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'start_vote': 1, 'end_vote': 1,
                 'votes': 1, 'candidates': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

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

        chat = 'freed0m0fspeech'
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
            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat}/{old_president}",
                          data=data, headers={'Origin': origin})
            # Promote new president
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'promote_chat_member',
                'parameters': {'custom_title': 'Президент'},
            }
            data = json.dumps(data)
            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat}/{president}",
                          data=data, headers={'Origin': origin})

        if parliament != document.get('parliament', ''):
            # Demote old parliament
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'demote_chat_member',
            }
            data = json.dumps(data)
            old_parliament = document.get('parliament', '')
            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat}/{old_parliament}",
                          data=data, headers={'Origin': origin})
            # Promote new parliament
            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                'action': 'promote_chat_member',
                'parameters': {'custom_title': 'Парламент'},
            }
            data = json.dumps(data)

            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat}/{parliament}",
                          data=data, headers={'Origin': origin})

        # Delete vote and votes information from database
        query = {'end_vote': '', 'votes': '', 'candidates': ''}
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

        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat}", data=data,
                      headers={'Origin': origin})
    except:
        pass


def scheduled_telegram_synching(start=0, stop=200, step=1):
    from .updater import sched

    sync_time = datetime.now(tz=utc) + timedelta(hours=4)
    sync_time = sync_time.strftime('%Y-%m-%d %H:%M:%S')

    sched.add_job(scheduled_telegram_synching, 'date', run_date=sync_time, id='scheduled_telegram_synching')
    # print('Scheduled Telegram Synching Running')
    try:
        chat = 'freed0m0fspeech'
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }
        data = json.dumps(data)
        origin = os.getenv('HOSTNAME', '')
        chat = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/chat/{chat}", data=data,
                            headers={'Origin': origin})

        if chat:
            chat = chat.json()

            query = {'chat': chat}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                       action='$set', query=query)

            time.sleep(60)

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

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
            telegram = tuser.get('telegram', {})

            if telegram:
                telegram_username = telegram.get('username', '')

                member = requests.get(
                    f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat}/{telegram_username}",
                    data=data, headers={'Origin': origin})
                # sync_count += 1

                print(member)

                if member:
                    member = member.json()

                    print(member)

                    query = {f'users.{user}.member': member}
                    mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                               action='$set', query=query)

                    # member_parameters = member.get('member_parameters', {})
                    # if member_parameters:
                    #     role = member_parameters.get('custom_title', '')
                    #     if role:
                    #         role = role.lower()
                    #
                    #         if role == 'судья':
                    #             if document.get('judge', '') != user:
                    #                 query = {f"judge": user}
                    #                 mongoDataBase.update_field(database_name='site',
                    #                                            collection_name='freedom_of_speech',
                    #                                            action='$set', query=query)
                    #
                    #         if role == 'президент':
                    #             if document.get('president', '') != user:
                    #                 query = {f"president": user}
                    #                 mongoDataBase.update_field(database_name='site',
                    #                                            collection_name='freedom_of_speech',
                    #                                            action='$set', query=query)
                    #
                    #         if role == 'парламент':
                    #             if document.get('parliament', '') != user:
                    #                 query = {f"parliament": user}
                    #                 mongoDataBase.update_field(database_name='site',
                    #                                            collection_name='freedom_of_speech',
                    #                                            action='$set', query=query)

                # if sync_count == stop:
                #     return

                # print(f'Synched {sync_count}')
                time.sleep(60)

    except:
        pass

    sched.print_jobs()
