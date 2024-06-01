import json
import logging
import os
import random
import requests

from datetime import datetime, timedelta
from apscheduler.jobstores.base import JobLookupError
from dateutil import tz
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from pytz import utc

import freedom_of_speech.utils
import portfolio.utils

load_dotenv()

from utils import dataBases, cache

mongoDataBase = dataBases.mongodb_client


def start_voting_later():
    from jobs.updater import sched
    start_vote = datetime.now(tz=utc) + timedelta(hours=1)
    start_vote = start_vote.strftime('%Y-%m-%d %H:%M:%S')

    job = sched.get_job('start_voting')
    if job:
        job.modify(next_run_time=start_vote)
    else:
        sched.add_job(start_voting, 'date', run_date=start_vote, id='start_voting',
                      misfire_grace_time=None, coalesce=True)
    return


def start_voting():
    from jobs.updater import sched

    if not mongoDataBase.check_connection():
        return start_voting_later()

    # query = {'_id': 0, 'candidates': 1, 'telegram': 1}
    # document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

    document = cache.freedom_of_speech

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

        mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                      action='$set', query=query)

        if mongoUpdate is None:
            return start_voting_later()
        else:
            cache.freedom_of_speech = mongoUpdate

        text = f"**Недостаточно кандидатов на выборы [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech | Выборы были перенесены**"

        chat_username = json.loads(document.get('telegram', {}).get('chat_parameters', {}).get('id', ''))
        origin = os.getenv('HOSTNAME', '')

        data = {
            "text": text,
            "pin": 'true',
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }

        data = json.dumps(data)
        telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

        requests.post(f"{telegram_api_endpoint}/send/{chat_username}", data=data)

        return

    end_vote = datetime.now(tz=utc) + timedelta(days=1)
    end_vote = end_vote.strftime('%Y-%m-%d %H:%M:%S')

    start_vote = datetime.now(tz=utc) + relativedelta(months=3)
    start_vote = start_vote.strftime('%Y-%m-%d 00:00:00')

    notify_vote = datetime.strptime(start_vote, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
    notify_vote = notify_vote.strftime('%Y-%m-%d %H:%M:%S')

    query = {'end_vote': f'{end_vote}', 'start_vote': f'{start_vote}'}

    mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                  action='$set', query=query)

    if mongoUpdate is None:
        return start_voting_later()
    else:
        cache.freedom_of_speech = mongoUpdate

    job = sched.get_job('end_voting')
    if job:
        job.modify(next_run_time=end_vote)
    else:
        sched.add_job(end_voting, 'date', run_date=end_vote, id='end_voting')

    job = sched.get_job('start_voting')
    if job:
        job.modify(next_run_time=start_vote)
    else:
        sched.add_job(start_voting, 'date', run_date=start_vote, id='start_voting')

    job = sched.get_job('notify_voting')
    if job:
        job.modify(next_run_time=notify_vote)
    else:
        sched.add_job(notify_voting, 'date', run_date=notify_vote, id='notify_voting')

    text = f"**В данный момент на [официальной странице]({os.getenv('HOSTNAME', '')}freedom_of_speech) проходят [выборы Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech**"

    chat_username = json.loads(document.get('telegram', {}).get('chat_parameters', {}).get('id', ''))
    origin = os.getenv('HOSTNAME', '')

    data = {
        "text": text,
        "pin": 'true',
        'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
    }

    data = json.dumps(data)
    telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

    requests.post(f"{telegram_api_endpoint}/send/{chat_username}", data=data)

    cache.freedom_of_speech = freedom_of_speech.utils.update_cached_data(mongoDataBase)


def end_voting_later():
    from jobs.updater import sched

    end_vote = datetime.now(tz=utc) + timedelta(hours=1)
    end_vote = end_vote.strftime('%Y-%m-%d %H:%M:%S')

    job = sched.get_job('end_voting')
    if job:
        job.modify(next_run_time=end_vote)
    else:
        sched.add_job(end_voting, 'date', run_date=end_vote, id='end_voting',
                      misfire_grace_time=None, coalesce=True)

    sched.print_jobs()

    return


def end_voting():
    if not mongoDataBase.check_connection():
        return end_voting_later()

    # query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'start_vote': 1, 'end_vote': 1,
    #          'votes': 1, 'candidates': 1, 'telegram': 1}
    # document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

    document = cache.freedom_of_speech

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

    chat_username = json.loads(document.get('telegram', {}).get('chat_parameters', {}).get('id', ''))
    origin = os.getenv('HOSTNAME', '')

    judge = document.get('judge', {}).get('judge', '')
    if president == judge or parliament == judge:
        query = {'judge': ''}
        mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                      action='$unset', query=query)

        if mongoUpdate is None:
            return end_voting_later()
        else:
            cache.freedom_of_speech = mongoUpdate

    if president != document.get('president', ''):
        # Demote old president
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            'action': 'demote_chat_member',
        }
        data = json.dumps(data)
        old_president = document.get('president', '')
        told_president = document.get('users', {}).get(old_president, {}).get('telegram', {}).get('id', '')
        tpresident = document.get('users', {}).get(president, {}).get('telegram', {}).get('id', '')
        telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

        response = requests.post(f"{telegram_api_endpoint}/manage/{chat_username}/{told_president}",
                      data=data)

        if not response.status_code == 200:
            logging.warning('Old president not demoted through Telegram API')

        # Promote new president
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            'action': 'promote_chat_member',
            'parameters': {'custom_title': 'Президент'},
        }
        data = json.dumps(data)
        telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

        response = requests.post(f"{telegram_api_endpoint}/manage/{chat_username}/{tpresident}",
                      data=data)

        if not response.status_code == 200:
            logging.warning('New president not promoted through Telegram API')

    if parliament != document.get('parliament', ''):
        # Demote old parliament
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            'action': 'demote_chat_member',
        }
        data = json.dumps(data)
        old_parliament = document.get('parliament', '')
        told_parliament = document.get('users', {}).get(old_parliament, {}).get('telegram', {}).get('id', '')
        tparliament = document.get('users', {}).get(parliament, {}).get('telegram', {}).get('id', '')
        telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

        response = requests.post(f"{telegram_api_endpoint}/manage/{chat_username}/{told_parliament}",
                      data=data)

        if not response.status_code == 200:
            logging.warning('Old parliament not demoted through Telegram API')

        # Promote new parliament
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            'action': 'promote_chat_member',
            'parameters': {'custom_title': 'Парламент'},
        }
        data = json.dumps(data)
        telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

        response = requests.post(f"{telegram_api_endpoint}/manage/{chat_username}/{tparliament}",
                      data=data)

        if not response.status_code == 200:
            logging.warning('New parliament not promoted through Telegram API')

    # Delete vote and votes information from database
    query = {'end_vote': '', 'votes': '', 'candidates': '', 'referendum.votes': ''}
    mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                  action='$unset', query=query)

    if mongoUpdate is None:
        return end_voting_later()
    else:
        cache.freedom_of_speech = mongoUpdate

    # Set new president, parliament in database
    query = {"parliament": parliament, 'president': president}
    mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                  action='$set', query=query)

    if mongoUpdate is None:
        logging.warning('New government not set in DataBase')
    else:
        cache.freedom_of_speech = mongoUpdate

    users = document.get('users', {})
    tpresident = users.get(president, {}).get('telegram', {}).get('id', '')
    tparliament = users.get(parliament, {}).get('telegram', {}).get('id', '')

    text = f"**Завершены выборы [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech:\n\n**"
    if tpresident:
        text = f"{text}Новый Президент: [{president}](tg://user?id={tpresident})\n"
    else:
        text = f"{text}Новый Президент: {president}\n"

    if tparliament:
        text = f"{text}Новый Парламент: [{parliament}](tg://user?id={tparliament})\n"
    else:
        text = f"{text}Новый Парламент: {parliament}\n"

    data = {
        "text": text,
        "pin": 'true',
        'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
    }

    data = json.dumps(data)
    telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

    requests.post(f"{telegram_api_endpoint}/send/{chat_username}", data=data)

    referendum_date = datetime.now(tz=utc)
    referendum_date = referendum_date.strftime('%Y-%m-%d %H:%M:%S')
    # Set new referendum be valid only after 30 days after vote
    query = {"referendum.date": referendum_date}
    mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                  query=query)

    if mongoUpdate is None:
        logging.warning('New referendum date not set in DataBase')
    else:
        cache.freedom_of_speech = mongoUpdate

    cache.freedom_of_speech = freedom_of_speech.utils.update_cached_data(mongoDataBase)


def telegram_synching(start=0, stop=200, step=1):
    from jobs.updater import sched

    if not mongoDataBase.check_connection():
        return

    # query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'referendum': 1, 'telegram': 1}
    # document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

    document = cache.freedom_of_speech

    if not document:
        return

    # last_update_chat = document.get('telegram', {}).get('chat_parameters', {}).get('date', '')
    #
    # if last_update_chat:
    #     last_update_seconds = (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update_chat,
    #                                                                                          '%Y-%m-%d %H:%M:%S')).total_seconds()
    # else:
    #     last_update_seconds = 14400
    #
    # # update only every 4 hours
    # if last_update_seconds >= 14400:

    chat_username = json.loads(document.get('telegram', {}).get('chat_parameters', {}).get('id', ''))
    data = {
        'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
    }
    data = json.dumps(data)
    origin = os.getenv('HOSTNAME', '')
    telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

    chat = requests.get(f"{telegram_api_endpoint}/chat/{chat_username}", data=data)

    if chat and chat.status_code == 200:
        chat = chat.json()

        query = {'telegram.chat_parameters': chat.get('chat_parameters', {}),
                 'telegram.members_parameters': chat.get('members_parameters', {})}
        mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                      action='$set', query=query)

        if mongoUpdate is None:
            return
        else:
            cache.freedom_of_speech = mongoUpdate

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
                    members_count = int(members_count)

                    # Count of referendum_true values
                    if (100 * float(len(referendum_usernames)) / float(
                            members_count - len(government))) >= document.get('referendum', {}).get('percent',
                                                                                                    75):

                        try:
                            sched.remove_job('start_voting')
                        except JobLookupError:
                            # job not found
                            pass

                        job = sched.get_job('start_voting')
                        if job:
                            job.modify(next_run_time=datetime.now(tz=utc))
                        else:
                            sched.add_job(start_voting, 'date', run_date=datetime.now(tz=utc),
                                          id='start_voting')

                        referendum_date = datetime.now(tz=utc)
                        referendum_date = referendum_date.strftime('%Y-%m-%d %H:%M:%S')

                        query = {'referendum.votes': '', 'referendum.date': referendum_date}
                        mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                   action='$set', query=query)

                        if mongoUpdate is None:
                            return
                        else:
                            cache.freedom_of_speech = mongoUpdate


def discord_synching(start=0, stop=200, step=1):
    if not mongoDataBase.check_connection():
        return

    # query = {'_id': 0, 'users': 1, 'discord': 1}
    # document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

    document = cache.freedom_of_speech

    if not document:
        return

    # last_update_guild = document.get('discord', {}).get('guild_parameters', {}).get('date', '')
    #
    # if last_update_guild:
    #     last_update_seconds = (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update_guild,
    #                                                                                          '%Y-%m-%d %H:%M:%S')).total_seconds()
    # else:
    #     last_update_seconds = 14400
    #
    # # update only every 4 hours
    # if last_update_seconds >= 14400:

    guild_id = document.get('discord', {}).get('guild_parameters', {}).get('id', '')
    data = {
        'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
    }
    data = json.dumps(data)
    origin = os.getenv('HOSTNAME', '')
    discord_api_endpoint = os.getenv('DISCORD_API_ENDPOINT', '')
    guild = requests.get(f"{discord_api_endpoint}/guild/{guild_id}", data=data)

    if guild and guild.status_code == 200:
        guild = guild.json()

        query = {'discord.guild_parameters': guild.get('guild_parameters', {}),
                 'discord.members_parameters': guild.get('members_parameters', {})}
        mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                   action='$set', query=query)

        if mongoUpdate is None:
            return
        else:
            cache.freedom_of_speech = mongoUpdate


def voting_later():
    from jobs.updater import sched

    date = datetime.now(tz=utc) + timedelta(minutes=15)
    date = date.strftime('%Y-%m-%d %H:%M:%S')

    job = sched.get_job('voting')
    if job:
        job.modify(next_run_time=date)
    else:
        sched.add_job(voting, 'date', run_date=date, id='voting', misfire_grace_time=None,
                      coalesce=True)
    return


def voting():
    from jobs.updater import sched

    if not mongoDataBase.check_connection():
        return voting_later()
    else:
        # query = {'_id': 0, 'start_vote': 1, 'end_vote': 1}
        # document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
        #                                       query=query)

        document = cache.freedom_of_speech

        # Start vote job (on start_vote date in db)
        start_vote = document.get('start_vote', '')
        end_vote = document.get('end_vote', '')

        if start_vote:
            job = sched.get_job('start_voting')
            if job:
                job.modify(next_run_time=start_vote)
            else:
                sched.add_job(start_voting, 'date', run_date=start_vote, id='start_voting',
                              misfire_grace_time=None, coalesce=True)

        # End vote job (on end_vote date in db)
        if end_vote:
            job = sched.get_job('end_voting')
            if job:
                job.modify(next_run_time=end_vote)
            else:
                sched.add_job(end_voting, 'date', run_date=end_vote, id='end_voting',
                              misfire_grace_time=None, coalesce=True)

    cache.freedom_of_speech = freedom_of_speech.utils.update_cached_data(mongoDataBase)


def notify_voting():
    document = cache.freedom_of_speech

    if not document:
        return

    start_vote = document.get('start_vote', '')
    if not start_vote:
        return

    start_vote = datetime.strptime(start_vote, '%Y-%m-%d %H:%M:%S')
    start_vote = start_vote.replace(tzinfo=tz.gettz('UTC'))

    # locale.setlocale(locale.LC_ALL, 'ru_RU')
    text = f"**{start_vote.astimezone(tz.gettz('Europe/Kiev')).strftime('%e.%m.%Y в %H:%M:%S')} на [официальной странице]({os.getenv('HOSTNAME', '')}freedom_of_speech) будут проходить [выборы Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech**"
    # locale.setlocale(locale.LC_ALL, '')

    chat_username = json.loads(document.get('telegram', {}).get('chat_parameters', {}).get('id', ''))
    origin = os.getenv('HOSTNAME', '')

    data = {
        "text": text,
        "pin": 'true',
        'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
    }

    data = json.dumps(data)
    telegram_api_endpoint = os.getenv('TELEGRAM_API_ENDPOINT', '')

    requests.post(f"{telegram_api_endpoint}/send/{chat_username}", data=data)


def sync():
    cache.portfolio = portfolio.utils.update_cached_data(mongoDataBase)
    cache.freedom_of_speech = freedom_of_speech.utils.update_cached_data(mongoDataBase)
