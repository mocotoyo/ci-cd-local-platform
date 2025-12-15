import logging
import json_log_formatter

formatter = json_log_formatter.JSONFormatter()

json_handler = logging.StreamHandler()
json_handler.setFormatter(formatter)

logger = logging.getLogger('my_logger')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

logger.info('App started', extra={"app_name": "app1"})

