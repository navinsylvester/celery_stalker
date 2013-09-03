celery_stalker
==============

If you worship logs and use celery - you would like this simple tool. Celery has few good real-time monitoring tools like flower, celerymon and celeryev. Celery is a critical component so it's necessary to have an archieve of what really happened and get it processed by splunk or other similar tools to raise alerts. You can use this tool to avoid going through hassles of sentry or other similar tools. Celery_stalker is based on celerymon skeleton but functionality is entirely different.

Usage
=====

python celery_stalker.py --config=cs_conf

[or]

python celery_stalker.py --config=cs_conf -D

