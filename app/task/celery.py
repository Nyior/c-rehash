# from __future__ import absolute_import

from celery import Celery


app = Celery('task', include=['app.task.tasks'])
app.config_from_object('app.task.celeryconfig')

if __name__ == '__main__':
    app.start()