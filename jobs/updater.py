from datetime import datetime, timedelta

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .jobs import scheduled_start_voting, scheduled_end_voting, scheduled_telegram_synching

from pytz import utc
from dotenv import load_dotenv

load_dotenv()

from utils import mongoDataBase

# executors = {
#     'default': ThreadPoolExecutor(1)
# }

sched = BackgroundScheduler(timezone=utc)


def start():
    query = {'_id': 0, 'start_vote': 1, 'end_vote': 1}
    document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

    start_vote = document.get('start_vote', '')
    if start_vote:
        sched.add_job(scheduled_start_voting, 'date', run_date=start_vote, id='scheduled_start_voting')

    end_vote = document.get('end_vote', '')
    if end_vote:
        sched.add_job(scheduled_end_voting, 'date', run_date=end_vote, id='scheduled_end_voting')

    # sched.add_job(scheduled_telegram_synching, 'date', run_date=datetime.now(tz=utc), id='scheduled_telegram_synching')

    sched.add_job(scheduled_telegram_synching, 'interval', hours=4, id='scheduled_telegram_synching')
    sched.get_job('scheduled_telegram_synching').modify(next_run_time=datetime.now(tz=utc))

    # schduler.add_job(test, 'date', run_date=datetime.now(tz=utc), args=['1', '2'])

    sched.start()

    sched.print_jobs()
