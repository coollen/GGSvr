# coding: utf-8
# 日志模块
import logging


LOG_FILE = "log.txt"

global logger


def init():
    global logger
    logger = logging.getLogger()
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)


def log(msg):
    global logger
    print msg
    logger.info(msg)


def info(msg):
    log(msg)


def debug(msg):
    global logger
    print msg
    logger.debug(msg)


def warning(msg):
    global logger
    print msg
    logger.warning(msg)


def error(msg):
    global logger
    print msg
    logger.error(msg)


# 打印对象属性
def print_object(obj):
    for key in obj.__dict__:
        print key + ' : ' + obj.__dict__[key]



