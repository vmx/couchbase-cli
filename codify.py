#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Try to use the couchbase-cli code to setup a cluster programatically
# which then could be described with cucumer

import json
import sys
import time

from node import Node
import util_cli as util


class Control:
    def __init__(self, server, port, user, password, ssl):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl

        self.debug = True
        self.node = Node()

    def cluster_init(self, ramsize_data, ramsize_index, services):
        cluster = '{}:{}'.format(self.server, self.port)
        cluster_username = self.user
        cluster_password = self.password
        cluster_port = self.port

        opts = [('--cluster', cluster),
                ('--cluster-username', cluster_username),
                ('--cluster-password', cluster_password),
                ('--cluster-port', str(cluster_port)),
                ('--cluster-ramsize', str(ramsize_data)),
                ('--cluster-index-ramsize', str(ramsize_index)),
                ('--services', services)]

        return self.node.runCmd('cluster-init', self.server, self.port,
                                self.user, self.password, self.ssl, opts)

    def server_add(self, servers):
        cluster = '{}:{}'.format(self.server, self.port)
        username = self.user
        password = self.password
        cluster_port = self.port

        opts = [('--cluster', cluster),
                ('-u', username),
                ('-p', password)]
        for server, config in servers.items():
            opts.append(('--server-add', server))
            opts.append(('--server-add-username', username))
            opts.append(('--server-add-password', password))
            opts.append(('--services', config['services']))

        self.node.runCmd('server-add', self.server, self.port, self.user,
                         self.password, self.ssl, opts)

    def rebalance(self):
        cluster = '{}:{}'.format(self.server, self.port)
        username = self.user
        password = self.password

        opts = [('--cluster', cluster),
                ('-u', username),
                ('-p', password)]

        self.node.runCmd('rebalance', self.server, self.port, self.user,
                         self.password, self.ssl, opts)

    def server_remove(self, servers):
        cluster = '{}:{}'.format(self.server, self.port)
        username = self.user
        password = self.password

        opts = [('--cluster', cluster),
                ('-u', username),
                ('-p', password)]

        for server in servers:
            opts.append(('--server-remove', server))
        print("vmx: server remove opts: {}".format(opts))
        self.node.runCmd('rebalance', self.server, self.port, self.user,
                         self.password, self.ssl, opts)

    def load_sample_data(self, dataset):
        rest = util.restclient_factory(self.server,
                                       self.port,
                                       {'debug':self.debug},
                                       self.ssl)
        rest.setPayload(json.dumps([dataset]))
        opts = {
            'success_msg': 'sample dataset was loaded',
            'error_msg': 'cannot load sample dataset'
        }
        rest.restCmd('POST',
                     '/sampleBuckets/install',
                     self.user,
                     self.password,
                     opts)

        opts = {
            'success_msg': 'sample dataset was loaded',
            'error_msg': 'cannot load sample dataset'
        }
        while True:
            time.sleep(10)
            rest = util.restclient_factory(self.server,
                                           self.port,
                                           {'debug':self.debug},
                                           self.ssl)
            output_result = rest.restCmd('GET',
                                         '/pools/default/tasks',
                                         self.user,
                                         self.password,
                                         opts)
            tasks = rest.getJson(output_result)
            for task in tasks:
                if task['type'] in ['loadingSampleBucket', 'indexer']:
                    if task["status"] == "running":
                        break
            else:
                return

        #curl 'http://emil:9000/sampleBuckets/install' -H 'Host: emil:9000' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'DNT: 1' -H 'Referer: http://emil:9000/index.html?na' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'invalid-auth-response: on' -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' -H 'ns_server-ui: yes' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: ui-auth-emil%3A9000=d848d1820afccfe90c846ae4baae1669' -H 'Connection: keep-alive' --data '["travel-sample"]'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    #cmd = 'cluster-init'
    server = '127.0.0.1'
    port =  9000
    user = 'Administrator'
    password = 'asdasd'
    ssl = False

    control = Control(server, port, user, password, ssl)

    ramsize_data = 512
    ramsize_index = 512
    services = 'data'
    control.cluster_init(ramsize_data, ramsize_index, services)

    servers = {'127.0.0.1:9001': {'services': 'data'},
               '127.0.0.1:9002': {'services': 'data'},
               '127.0.0.1:9003': {'services': 'data'}}
    control.server_add(servers)

    control.rebalance()

    control.load_sample_data('travel-sample')
    control.server_remove(['127.0.0.1:9002'])

#    opts = [('--cluster', '127.0.0.1:9000'), ('--cluster-username', 'Administrator'), ('--cluster-password', 'asdasd'), ('--cluster-port', '9000'), ('--clustr-ramsize', '512'), ('--cluster-index-ramsize', '512'), ('--services', 'data')]
#    control.cluster_init(opts)
#
#    opts = [('--cluster', '127.0.0.1:9000'), ('-u', 'Administrator'), ('-p', 'asdasd'), ('--server-add', '127.0.0.1:9001'), ('--services', 'data'), ('--server-add', '127.0.0.1:9002'), ('--services', 'data'), ('--server-add', '127.0.0.1:9003'), ('--services', 'data')]
#    control.server_add(opts)
#
#
#    opts = [('--cluster', '127.0.0.1:9000'), ('-u', 'Administrator'), ('-p', 'asdasd')]
#    control.rebalance(opts)



#    node = Node()
#
#    opts = [('--cluster', '127.0.0.1:9000'), ('--cluster-username', 'Administrator'), ('--cluster-password', 'asdasd'), ('--cluster-port', '9000'), ('--cluster-ramsize', '512'), ('--cluster-index-ramsize', '512'), ('--services', 'data')]
#    node.runCmd(cmd, server, port, user, password, ssl, opts)
#
#
#    cmd = 'server-add'
#    opts = [('--cluster', '127.0.0.1:9000'), ('-u', 'Administrator'), ('-p', 'asdasd'), ('--server-add', '127.0.0.1:9001'), ('--services', 'data'), ('--server-add', '127.0.0.1:9002'), ('--services', 'data'), ('--server-add', '127.0.0.1:9003'), ('--services', 'data')]
#    node.runCmd(cmd, server, port, user, password, ssl, opts)
#
#
#    cmd = 'rebalance'
#    opts = [('--cluster', '127.0.0.1:9000'), ('-u', 'Administrator'), ('-p', 'asdasd')]
#    node.runCmd(cmd, server, port, user, password, ssl, opts)


#vmx: cmd, opts: cluster-init, [('--cluster', '127.0.0.1:9000'), ('--cluster-username', 'Administrator'), ('--cluster-password', 'asdasd'), ('--cluster-port', '9000'), ('--cluster-ramsize', '512'), ('--cluster-index-ramsize', '512'), ('--services', 'data')]
#vmx: cmd, opts: server-add, [('--cluster', '127.0.0.1:9000'), ('-u', 'Administrator'), ('-p', 'asdasd'), ('--server-add', '127.0.0.1:9001'), ('--services', 'data'), ('--server-add', '127.0.0.1:9002'), ('--services', 'data'), ('--server-add', '127.0.0.1:9003'), ('--services', 'data')]
#vmx: cmd, opts: rebalance, [('--cluster', '127.0.0.1:9000'), ('-u', 'Administrator'), ('-p', 'asdasd')]



    print("Hello World!")

if __name__ == '__main__':
    sys.exit(main())
