import logging
import logging.handlers
import os
import sys
import time


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class Log4test(object):
    def __init__(self):
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(level=logging.DEBUG)
        while self.logger.hasHandlers():
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)

        # 创建文件目录
        logs_dir = os.path.dirname(__file__)+"/../logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)

        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        file_name = 'log_%s.txt' % timestamp
        file_path = os.path.join(logs_dir, file_name)

        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(process)d-%(threadName)s-%(thread)d] [%('
                                      'module)s.py:%(lineno)d] --> %(message)s', '%Y-%m-%d %H:%M:%S')

        file_handler = logging.handlers.RotatingFileHandler(filename=file_path,
                                                            maxBytes=1024 * 1024 * 50,
                                                            backupCount=5)
        file_handler.setFormatter(formatter)

        # 控制台句柄
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)

        # 添加内容到日志句柄中
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)


if __name__ == '__main__':
    log_wrapper = Log4test()
    log_wrapper.info("this is info")
    log_wrapper.debug("this is debug")
    log_wrapper.error("this is error")
    log_wrapper.warning("this is warning")
