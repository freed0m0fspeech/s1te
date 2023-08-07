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
    scheduled_start_voting,
    scheduled_end_voting,
    scheduled_telegram_synching,
    scheduled_discord_synching,
    scheduled_voting
)
from pytz import utc
from dotenv import load_dotenv

load_dotenv()

from utils import dataBases

mongoDataBase = dataBases.mongodb_client


# executors = {
#     'default': ThreadPoolExecutor(1)
# }

def listener(event):
    if event.exception:
        # print('The job crashed :(')
        # print(event.job_id)
        pass
    else:
        # print('The job worked :)')
        pass


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

        sched.add_job(scheduled_voting, 'date', run_date=date, id='scheduled_voting',
                      misfire_grace_time=None, coalesce=True)
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

    # Referendum check job (every day)
    # sched.add_job(scheduled_referendum_check, 'interval', days=1, id='scheduled_referendum_check')

    # Telegram synch job and referendum check (every 4 hours)
    sched.add_job(scheduled_telegram_synching, 'interval', hours=4, id='scheduled_telegram_synching',
                  misfire_grace_time=None, coalesce=True)

    # Discord synch job (every 4 hours)
    sched.add_job(scheduled_discord_synching, 'interval', hours=4, id='scheduled_discord_synching',
                  misfire_grace_time=None, coalesce=True)

    # sched.get_job('scheduled_telegram_synching').modify(next_run_time=datetime.now(tz=utc))
    # schduler.add_job(test, 'date', run_date=datetime.now(tz=utc), args=['1', '2'])

    sched.start()

    sched.print_jobs()
