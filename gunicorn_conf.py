# pylint: disable=invalid-name
from multiprocessing import cpu_count


def max_workers():
    return 2 * cpu_count() + 1


workers = max_workers()
worker_class = 'gevent'
accesslog = "logs/gunicorn_access.log"
access_log_format = "%(h)s %({X-Real-IP}i)s %(D)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = "logs/gunicorn_error.log"
