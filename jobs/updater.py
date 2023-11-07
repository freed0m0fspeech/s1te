# from datetime import datetime, timedelta
# from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime, timedelta

from apscheduler.events import (
    EVENT_JOB_EXECUTED,
    EVENT_JOB_ERROR
)
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.jobs import (
    start_voting,
    end_voting,
    telegram_synching,
    discord_synching,
    voting,
    sync
)
from pytz import utc
from dotenv import load_dotenv

load_dotenv()

from utils import dataBases, cache

mongoDataBase = dataBases.mongodb_client


# executors = {
#     'default': ThreadPoolExecutor(1)
# }

def listener(event):
    if event.exception:
        print(f'The job {event.job_id}() crashed :(')
    else:
        print(f'The job {event.job_id}() executed successfully :)')
        # sched.print_jobs()


job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': None,
}

sched = BackgroundScheduler(timezone=utc, job_defaults=job_defaults)
sched.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


def start():
    if not mongoDataBase.check_connection():
        date = datetime.now(tz=utc) + timedelta(minutes=15)
        date = date.strftime('%Y-%m-%d %H:%M:%S')

        sched.add_job(voting, 'date', run_date=date, id='voting',
                      misfire_grace_time=None, coalesce=True)
    else:
        # query = {'_id': 0, 'start_vote': 1, 'end_vote': 1}
        # document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        document = cache.freedom_of_speech

        # Start vote job (on start_vote date in db)
        start_vote = document.get('start_vote', '')
        end_vote = document.get('end_vote', '')

        if start_vote:
            sched.add_job(start_voting, 'date', run_date=start_vote, id='start_voting',
                          misfire_grace_time=None, coalesce=True)

        # End vote job (on end_vote date in db)
        if end_vote:
            sched.add_job(end_voting, 'date', run_date=end_vote, id='end_voting',
                          misfire_grace_time=None, coalesce=True)

    # Referendum check job (every day)
    # sched.add_job(referendum_check, 'interval', days=1, id='referendum_check')

    # Telegram synch job and referendum check (every 4 hours)
    sched.add_job(telegram_synching, 'interval', hours=4, id='telegram_synching',
                  misfire_grace_time=None, coalesce=True)

    # Discord synch job (every 4 hours)
    sched.add_job(discord_synching, 'interval', hours=4, id='discord_synching',
                  misfire_grace_time=None, coalesce=True)

    # DataBase info sync
    sched.add_job(sync, 'interval', days=1, id='sync', misfire_grace_time=None, coalesce=True)

    # sched.get_job('telegram_synching').modify(next_run_time=datetime.now(tz=utc))
    # sched.get_job('discord_synching').modify(next_run_time=datetime.now(tz=utc))
    # sched.get_job('sync').modify(next_run_time=datetime.now(tz=utc))
    # schduler.add_job(test, 'date', run_date=datetime.now(tz=utc), args=['1', '2'])

    sched.start()

    sched.print_jobs()
