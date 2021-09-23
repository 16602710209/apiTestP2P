import logging
import os
from logging import handlers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://user-p2p-test.itheima.net'


def init_log_config():
    # 创建日志器
    logger = logging.getLogger()#初始化日志器对象
    logger.setLevel(logging.INFO)# 设置日志级别：表示比INFO级别高（包括INFO的日志信息才记录下来）
    # 创建控制台处理器
    sh = logging.StreamHandler() #负责将日志信息输入到Pycharm下方的console窗口中
    # 创建文件处理器
    logfile = BASE_DIR+os.sep+"log"+os.sep+"p2p{}.log".format("%Y%m%D %H%M%S")
    fh = logging.handlers.TimedRotatingFileHandler(logfile,when='M', interval=5, backupCount=5, encoding='UTF-8')
    # 设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)]-%(message)s'
    formatter = logging.Formatter(fmt)
    # 将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 把处理器添加到日志器中
    logger.addHandler(sh)
    logger.addHandler(fh)
