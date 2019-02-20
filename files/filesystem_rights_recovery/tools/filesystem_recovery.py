#!/bin/python
# encoding:utf8

import ConfigParser
# import logging
import json
import codecs
import os
import sys
import shutil
# from loguru import logger
from logbook import Logger, TimedRotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)


class NodesDiscovery:

    def __init__(self):
        handler = TimedRotatingFileHandler('../logs/filesystem_recovery.log')
        handler.push_application()
        self.logger = Logger(name='filesystem recovery')

        self.node_hosts, self.nodes_port, self.file_sd_filename = self.get_conf()
        self.nodes = {}
        self.ips = {}
        self.nodes_list = []
        self.ips_list = []

    @staticmethod
    def get_conf():
        ##从配置文件获取配置
        cp = ConfigParser.ConfigParser()
        with codecs.open(os.path.join(BASE_DIR, './config/config.ini'), 'r', encoding='utf-8') as f:
            cp.readfp(f)
            node_hosts = eval(cp.get('nodes', 'node_hosts').strip())
            nodes_port = int(cp.get('nodes', 'node_port').strip())
            file_sd_filename = cp.get('file_ds', 'file_sd_filename').strip()

        return node_hosts, nodes_port, os.path.join(BASE_DIR, file_sd_filename)

    def node_scaner(self, ip_range):
        port_scaner = nmap.PortScanner()
        try:
            # 调用扫描方法，参数指定扫描主机hosts，nmap扫描命令行参数arguments
            port_scaner.scan(hosts=ip_range, arguments=' -v -sS -p ' + str(self.nodes_port))
        except Exception as e:
            self.logger.error("Scan erro:" + str(e))
        self.logger.info('nmap port scanner finished!')

        for host in port_scaner.all_hosts():  # 遍历扫描主机
            self.logger.debug(port_scaner[host])
            if port_scaner[host]['status']['state'] == 'up':
                host = port_scaner[host]['addresses']['ipv4']
                try:
                    nodes_state = port_scaner[host]['tcp'][9100]['state']
                    ssh_state = port_scaner[host]['tcp'][22]['state']
                except Exception as e:
                    self.logger.error('Error while get state of host %s: %s' % (host, e))
                    continue
                else:
                    self.logger.debug("Host %s %s is %s" % (str(host), str(self.nodes_port), str(nodes_state)))
                    self.logger.debug("Host %s %s is %s" % (str(host), str(22), str(ssh_state)))
                    if nodes_state == 'open' and ssh_state == 'open':
                        self.nodes_list.append(host + ':' + str(self.nodes_port))
                        self.ips_list.append(host)

                        # self.nodes[group_name].append(host + ':' + str(self.nodes_port))
                        # self.ips[group_name].append(host)
                        # self.logger.debug('debug info of nodes: [group: %s, ip: %s]' % (group_name, host))
                        self.logger.debug('debug info of nodes: [ip: %s]' % host)
        self.logger.info('Finished for ips %s' % ip_range)

    def host_to_file_sd(self, hosts_list):
        hosts_conf = json.load(open(self.file_sd_filename, 'r'))

        # node_hosts = hosts_conf[0]['targets']
        # logger.info('Nodes hosts already found: %s' % node_hosts)

        self.logger.info('Latest nodes hosts: %s' % hosts_list)

        for hosts in hosts_conf:
            if hosts['labels']['job'] == 'nodes':
                nodes_list = hosts['targets']
                self.logger.debug('Nodes before update: %s' % nodes_list)
                self.logger.debug('Nodes updated: %s' % hosts_list)
                nodes_all = list(set(hosts_list))
                hosts['targets'] = nodes_all


            # count = 0
            # for hosts in hosts_conf:
            #     if hosts['labels']['hosts_group'] == group_name:
            #         hosts['targets'] = hosts_dict[group_name]
            #         break
            #     else:
            #         count += 1
            # if count == len(hosts_conf):
            #     new_group = {
            #         "labels": {
            #             "job": "nodes",
            #             "hosts_group": group_name
            #         },
            #         "targets": hosts_dict[group_name]}
            #     hosts_conf.append(new_group)

        hosts_file = json.dumps(hosts_conf, indent=4, ensure_ascii=False, sort_keys=False, encoding='utf-8')
        try:
            with open(self.file_sd_filename, 'w') as f:
                f.write(hosts_file)
        except Exception as e:
            self.logger.info('Write node_exporter info failed: %s' % e)
        else:
            shutil.copy(self.file_sd_filename, '../../file_ds/nodes.json')

    def node_scan(self):
        self.logger.info('hosts groups from configure file: %s' % self.node_hosts)

        for ip_range in self.node_hosts:
            self.logger.debug('Scan ip range %s' % ip_range)
            if ip_range:
                self.node_scaner(ip_range)

            # host_check = HostCheck(group_name, self.ips[group_name])
            # installed_hosts, missed_hosts = host_check.get_hosts()

            # if installed_hosts:
            #
            #     for host in installed_hosts:
            #         if group_name != 'windows':
                    # node_hosts_dict[group_name].append(host + ':' + str(self.nodes_port))
                    # # else:
                    # #     node_hosts_dict[group_name].append(host + ':' + str(self.win_nodes_port))

            # else:
            #     self.logger.error('Error! Please check log of host_check')
        if self.nodes_list:
            self.host_to_file_sd(self.nodes_list)
            self.logger.info('We finished here!')


if __name__ == '__main__':
    print('Nodes discovery started')
    nodes_discover = NodesDiscovery()
    nodes_discover.node_scan()
    print('Nodes discovery finished')
