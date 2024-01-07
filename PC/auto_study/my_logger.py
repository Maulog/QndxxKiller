import logging

class Logger:
    def __init__(self, name, log_file, level=logging.DEBUG):
        # 创建一个logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)

        # 定义handler的输出格式
        fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(fh_formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)

    def log(self, message, level=logging.INFO):
        # 记录一条日志
        self.logger.log(level, message)

