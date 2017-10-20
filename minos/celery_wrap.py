from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY']['result_backend'],
                    broker=app.config['CELERY']['broker_url'])
    celery.conf.update(app.config['CELERY'])
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery