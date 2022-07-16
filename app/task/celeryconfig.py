from celery.schedules import crontab


broker_url = 'redis://localhost:6379/1'
result_backend = 'redis://localhost:6379/1'


beat_schedule = {
    'fetch-rates': {
        'task': 'app.task.tasks.update_rates',
        'schedule': crontab(hour='*', minute='*', day_of_week='*')
    },
}

timezone = 'Africa/Lagos'
