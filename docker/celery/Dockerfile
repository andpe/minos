FROM minos/uwsgi

RUN python3 -m pip install celery redis

CMD ["/usr/local/bin/celery", "-l", "INFO", "-A", "minos.tasks.celery", "worker", "-B"]