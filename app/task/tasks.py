# from __future__ import absolute_import
import time
from app.task.celery import app
from app.config.settings import get_settings
from app.services.convert import get_rates


@app.task
def update_rates():
    settings = get_settings()
    url: str = settings.OPEN_API_RATES
    rates: dict = get_rates(url)
    print(f"RATES: {rates}")


@app.task
def send_welcome_email(user_email: str):
    time.sleep(5)
    print(f"\n Welcome email sent to {user_email} \n")
