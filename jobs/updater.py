from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import scheduled_start_voting, scheduled_end_voting, scheduled_telegram_synching
from pytz import utc


def start():
    schduler = BackgroundScheduler(timezone=utc)

    # schduler.add_job(scheduled_test, 'interval', seconds=5)
    schduler.add_job(scheduled_start_voting, 'cron', month='1, 4, 7, 10', day='last')
    schduler.add_job(scheduled_end_voting, 'cron', month='2, 5, 8, 11', day='1')
    schduler.add_job(scheduled_telegram_synching, 'interval', days=1)
    # schduler.add_job(scheduled_start_voting, 'cron', second='15')
    # schduler.add_job(scheduled_end_voting, 'cron', minute='1')

    schduler.start()

    # schduler.print_jobs()
