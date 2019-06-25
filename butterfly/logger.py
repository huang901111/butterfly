#coding:utf8

from xlib.logger import LoggerBase
import config

critlog = LoggerBase(config.PATH_CRIT_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

errlog = LoggerBase(config.PATH_ERR_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

warninglog = LoggerBase(config.PATH_WARNING_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

infolog = LoggerBase(config.PATH_INFO_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

acclog = LoggerBase(config.PATH_ACC_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)
