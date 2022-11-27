from multiprocessing import cpu_count

# Socket Path
bind = '/var/www/messages-api/gunicorn.sock'

# Worker Options
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = '/var/www/messages-api/logs/access_log'
errorlog = '/var/www/messages-api/logs/error_log'

# Reload options
reload = True
reload_engine = "auto"