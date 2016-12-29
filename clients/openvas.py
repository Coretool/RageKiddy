import sys
from time import sleep
sys.path.append('./')


def generate_name(type, nr):
    return 'Chameleon_{0}_{1}'.format(type, nr)


class OpenvasClient(object):
    def __init__(self, username, password, client, host):
        self.username = username
        self.password = password
        self.host = host
        self.client = client

    def load(self):
        self.client.console_execute('load openvas \n')
        response = self.client.console_read()
        while 'loaded' not in response:
            sleep(10)
            response = self.client.console_read()
        return True

    def connect(self):
        self.client.console_execute('openvas_connect {0} {1} {2} 9390 ok\n'.format(self.username, self.password,
                                                                                   self.host))
        response = self.client.console_read()
        while 'successful' not in response:
            sleep(10)
            response = self.client.console_execute()
        return True

    def scan(self, target, audit=3, index=1):
        name = generate_name(index)  # TODO change this to be useable more than once
        self.client.console_execute('openvas_target_create "{0}" {1} "Chameleon Scan"\n'.format(name, target))
        sleep(3.141)  # yes, that's pi
        self.client.console_execute('openvas_task_create {0} "" {1} {2} {3}\n'.format(name, audit, index))
        self.client.console_execute('openvas_task_start 0')
        response = str(self.client.console_execute()[b'data'])
        while not 'Done' in response:
            sleep(10)
            response = str(self.client.console_execute()[b'data'])
        return True

