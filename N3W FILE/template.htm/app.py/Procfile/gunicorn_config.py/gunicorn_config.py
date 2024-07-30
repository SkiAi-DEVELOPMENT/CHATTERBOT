# gunicorn_config.py

# The address and port Gunicorn will bind to
bind = "0.0.0.0:8000"

# Number of worker processes Gunicorn will spawn
workers = 3

# The type of workers to use (sync is the default)
worker_class = "sync"

# Timeout for each worker
timeout = 30

# Log level
loglevel = "info"

# Access log file location (set to '-' to log to stdout)
accesslog = "-"

# Error log file location (set to '-' to log to stderr)
errorlog = "-"
