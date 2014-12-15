import os
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)

LOGGING = {
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'recommend.data_manage_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs','data_manage.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'recommend.data_manage': {
            'handlers': ['recommend.data_manage_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

import logging
handler_dict = {}

def touch_file(filename):
    if not os.path.exists(filename):
        os.system('mkdir %s -p' % os.path.dirname(filename))
        os.system('touch %s' % filename)

#######################################
# load all handlers in LOGGING to handler_list
#######################################
def load_handler():
    for handler_name, handler_conf in LOGGING['handlers'].items():
        level = handler_conf['level']
        filename = handler_conf['filename']
        format_str = LOGGING['formatters'][handler_conf['formatter']]['format']
        touch_file(filename)
        fh = logging.FileHandler(filename)
        if 'NOTSET' == level:
            fh.setLevel(logging.NOTSET)
        if 'DEBUG' == level:
            fh.setLevel(logging.DEBUG)
        elif 'INFO' == level:
            fh.setLevel(logging.INFO)
        elif 'WARNING' == level:
            fh.setLevel(logging.WARNING)
        elif 'ERROR' == level:
            fh.setLevel(logging.ERROR)
        elif 'CRITICAL' == level:
            fh.setLevel(logging.CRITICAL)
        formatter = logging.Formatter(format_str)
        fh.setFormatter(formatter)
        handler_dict[handler_name] = fh

#######################################
# load all loggers in LOGGING
#######################################
def load_log():
    for log_name, log_conf in LOGGING['loggers'].items():
        logger = logging.getLogger(log_name)
        level = log_conf['level']
        if 'NOTSET' == level:
            logger.setLevel(logging.NOTSET)
        if 'DEBUG' == level:
            logger.setLevel(logging.DEBUG)
        elif 'INFO' == level:
            logger.setLevel(logging.INFO)
        elif 'WARNING' == level:
            logger.setLevel(logging.WARNING)
        elif 'ERROR' == level:
            logger.setLevel(logging.ERROR)
        elif 'CRITICAL' == level:
            logger.setLevel(logging.CRITICAL)
        handlers = log_conf['handlers']
        for handler_name in handlers:
            logger.addHandler(handler_dict[handler_name])

load_handler()
load_log()

