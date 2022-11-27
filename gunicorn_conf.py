from multiprocessing import cpu_count

# Socket Path
bind = '/var/www/messages-api/gunicorn.sock'

# Worker Options
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/var/www/messages-api/logs/access_log'
errorlog = '/var/www/messages-api/logs/error_log'
