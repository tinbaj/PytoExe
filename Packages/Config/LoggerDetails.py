# LoggerDetails.py
"""
This is a file to create and initialize a logger
"""
import os
import logging

class LoggerDetails:
    """
    This is a class to create a logger and return this to the calling function
    """
    def __init__(self):
        self.log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logger.config')
        print(self.log_file_path)
    def setLogger(self):
        """
        This function gets the logger:myAppLogger and returns to the calling Function
        :return: Object of Logger: myAppLogger
        """
        #Setting Logger Parameters

        # create logger
        logger = logging.getLogger('myAppLogger')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.FileHandler(filename="C:/Users/user/PycharmProjects/PytoExe/log/myApp.log")
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # 'application' code
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')
        ###3
        return logger
    def __call__(self, *args, **kwargs):
        return self;