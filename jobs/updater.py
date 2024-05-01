import json
import logging
import os
import requests

from datetime import datetime, timedelta
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from dotenv import load_dotenv
from utils import dataBases, cache
from jobs.jobs import start_voting, end_voting, telegram_synching, discord_synching, voting, sync, notify_voting

load_dotenv()
mongoDataBase = dataBases.mongodb_client

# Constants for Job IDs
VOTING_JOB_ID = 'voting'
START_VOTING_JOB_ID = 'start_voting'
END_VOTING_JOB_ID = 'end_voting'
NOTIFY_VOTING_JOB_ID = 'notify_voting'
TELEGRAM_SYNCHING_JOB_ID = 'telegram_synching'
DISCORD_SYNCHING_JOB_ID = 'discord_synching'
SYNC_JOB_ID = 'sync'


def listener(event):
    if event.exception:
        logging.warning(f'The job {event.job_id}() crashed :(')
    else:
        logging.info(f'The job {event.job_id}() executed successfully :)')


job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': None,  # Run even if late (every sched must run)
}

sched = BackgroundScheduler(timezone=utc, job_defaults=job_defaults)
sched.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


def add_scheduled_job(func, trigger_type, **kwargs):
    """
    Helper function to add a scheduled job.
    """
    sched.add_job(func, trigger_type, **kwargs)

def setup_jobs():
    """
    Function to set up scheduled jobs.
    """
    if not mongoDataBase.check_connection():
        date = datetime.now(tz=utc) + timedelta(minutes=15)
        date = date.strftime('%Y-%m-%d %H:%M:%S')

        add_scheduled_job(voting, 'date', run_date=date, id=VOTING_JOB_ID, misfire_grace_time=None, coalesce=True)
    else:
        document = cache.freedom_of_speech

        start_vote = document.get('start_vote', '')
        end_vote = document.get('end_vote', '')

        if start_vote:
            add_scheduled_job(start_voting, 'date', run_date=start_vote, id=START_VOTING_JOB_ID,
                              misfire_grace_time=None, coalesce=True)

            notify_vote = datetime.strptime(start_vote, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
            notify_vote = notify_vote.strftime('%Y-%m-%d %H:%M:%S')

            if notify_vote > datetime.now(tz=utc).strftime('%Y-%m-%d %H:%M:%S'):
                add_scheduled_job(notify_voting, 'date', run_date=notify_vote, id=NOTIFY_VOTING_JOB_ID, misfire_grace_time=None, coalesce=True)

        if end_vote:
            add_scheduled_job(end_voting, 'date', run_date=end_vote, id=END_VOTING_JOB_ID, misfire_grace_time=None,
                              coalesce=True)

    add_scheduled_job(telegram_synching, 'interval', hours=4, id=TELEGRAM_SYNCHING_JOB_ID, misfire_grace_time=None,
                      coalesce=True)
    add_scheduled_job(discord_synching, 'interval', hours=4, id=DISCORD_SYNCHING_JOB_ID, misfire_grace_time=None,
                      coalesce=True)
    add_scheduled_job(sync, 'interval', days=1, id=SYNC_JOB_ID, misfire_grace_time=None, coalesce=True)


def start():
    """
    Start the scheduler and print job details.
    """
    setup_jobs()
    sched.start()
    sched.print_jobs()

    # sched.get_job('telegram_synching').modify(next_run_time=datetime.now(tz=utc))
    # sched.get_job('discord_synching').modify(next_run_time=datetime.now(tz=utc))
    # sched.get_job('sync').modify(next_run_time=datetime.now(tz=utc))
    # schduler.add_job(test, 'date', run_date=datetime.now(tz=utc), args=['1', '2'])
