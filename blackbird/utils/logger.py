#!/usr/bin/env python
# -*- encodig: utf-8 -*-

import logging
import logging.handlers


def logger_factory(filename, level, fmt='ltsv'):

    logger = logging.getLogger('blackbird')

    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }
    logger.setLevel(levels.get(level))

    handler = logging.handlers.WatchedFileHandler(filename, encoding='UTF-8', delay=True)
    formats = {
        'ltsv': ("log_level:%(levelname)s\t"
                 "time:%(asctime)s\t"
                 "process:%(name)s\t"
                 "thread:%(threadName)s\t"
                 "message:%(message)s"
                 )
    }
    datefmt = "%d/%b/%Y:%H:%M:%S %z"
    format = formats.get(fmt)
    formatter = logging.Formatter(fmt=format, datefmt=datefmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
