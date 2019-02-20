#!/bin/python
# encoding:utf8

import ConfigParser
import codecs
import os
import sys
import subprocess
import re
from logbook import Logger, TimedRotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)


class DeleteFiles:

    def __init__(self):
        handler = TimedRotatingFileHandler('../logs/delete_files.log')
        handler.push_application()
        self.logger = Logger(name='delete files')

        self.path_lists = self.get_conf()

    @staticmethod
    def get_conf():
        ##从配置文件获取配置
        cp = ConfigParser.ConfigParser()
        with codecs.open(os.path.join(BASE_DIR, './config/config.ini'), 'r', encoding='utf-8') as f:
            cp.readfp(f)
            path_lists = eval(cp.get('filesystem', 'del_paths').strip())

        return path_lists

    def file_handler(self):
        for file_path in self.path_lists:
            file_name = os.path.join('/', file_path)
            if os.path.isdir(file_name) or os.path.isfile(file_name):
                if os.path.isdir(file_name):
                    try:
                        os.removedirs(file_name)
                        #os.remove(file_name)
                    except Exception, e:
                        self.logger.error('Delete dir %s failed!%s' % (file_name, e))
                    else:
                        self.logger.info('Delete dir %s success!' % file_name)
                if os.path.isfile(file_name):
                    try:
                        #os.removedirs(file_name)
                        os.remove(file_name)
                    except Exception, e:
                        self.logger.error('Delete file %s failed!%s' % (file_name, e))
                    else:
                        self.logger.info('Delete file %s success!' % file_name)
            else:
                self.logger.info('%s not exists!' % file_name)
        self.logger.info('Delete finished!')


if __name__ == '__main__':
    print('Files delete started')
    delete_file = DeleteFiles()
    delete_file.file_handler()
    print('Files delete finished')
