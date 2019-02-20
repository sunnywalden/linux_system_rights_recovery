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


class RightsRecover:

    def __init__(self):
        handler = TimedRotatingFileHandler('../logs/filesystem_recovery.log')
        handler.push_application()
        self.logger = Logger(name='filesystem recovery')

        self.path_lists, regex_express = self.get_conf()
        self.reg_express = re.compile(regex_express)
        self.tmp_path = os.path.join(BASE_DIR, 'data')
        self.file_title = '.walden'

    @staticmethod
    def get_conf():
        ##从配置文件获取配置
        cp = ConfigParser.ConfigParser()
        with codecs.open(os.path.join(BASE_DIR, './config/config.ini'), 'r', encoding='utf-8') as f:
            cp.readfp(f)
            path_lists = eval(cp.get('filesystem', 'paths').strip())
            regex_express = eval(cp.get('filesystem', 'regex').strip())

        return path_lists, regex_express

    def file_handler(self, func):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
        for file_path in self.path_lists:

            if file_path != 'proc':
                file_name = os.path.join('/', file_path)
                back_file = os.path.join(self.tmp_path, file_path + self.file_title)
                func(file_name, back_file)
            else:
                files = os.listdir('/proc')
                for f_path in files:

                    if not self.reg_express.match(f_path):
                        file_name = os.path.join('/proc', f_path)
                        back_file = os.path.join(self.tmp_path, file_path + '_' + f_path + self.file_title)
                        func(file_name, back_file)

    def cmd_runner(self, cmd, file_path, cmd_type):
        #os.chdir('/')
        acl_runner = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/')
        out, err = acl_runner.communicate()
        if err:
            self.logger.error('%s ACL of path %s failed! %s' % (cmd_type, file_path, err))
        else:
            self.logger.info('%s ACL of path %s success!%s' % (cmd_type, file_path, out))

    def rights_backup(self, file_name, back_file):
        # file_name = os.path.join('/', file_path)
        # back_file = os.path.join(self.tmp_path, file_path + self.file_title)
        back_cmd = "getfacl  -R " + file_name + " > " + back_file
        self.cmd_runner(back_cmd, file_name, 'backup')

    def rights_restore(self, file_name, back_file):
        # file_name = os.path.join('/', file_path)
        # back_file = os.path.join(self.tmp_path, file_path + self.file_title)
        restore_cmd = "setfacl --restore=" + back_file
        self.cmd_runner(restore_cmd, file_name, 'restore')


handler = TimedRotatingFileHandler('../logs/filesystem_recovery.log')
handler.push_application()
logger = Logger(name='filesystem recovery')


def backup():
    logger.info('Files rights backup started')
    file_recover = RightsRecover()
    file_recover.file_handler(file_recover.rights_backup)
    logger.info('Files rights backup finished')


def restore():
    logger.info('Files rights restore started')
    file_recover = RightsRecover()
    file_recover.file_handler(file_recover.rights_restore)
    logger.info('Files rights restore finished')


if __name__ == '__main__':
    args_num = len(sys.argv) - 1
    if args_num == 1:
        if str(sys.argv[1]).strip() == "backup":
            backup()
        elif str(sys.argv[1]).strip() == "restore":
            restore()
        else:
            logger.info('Wrong function been given, deliver backup instead')
            backup()
    else:
        logger.info('No param been given, backup delivered')
        backup()
