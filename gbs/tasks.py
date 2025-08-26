from celery import shared_task
from gbs.utils import get_season  # Adjust import to your function's location
from datetime import date

@shared_task
def check_season_task():
    today = date.today()
    if today.day == 1:
        season = get_season()
        print(f"The season is: {season}")
        # Add any additional logic, like saving to a database


