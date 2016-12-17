from time import sleep
from . import metasploit

# TODO finish, add cleanup

def generate_name(type, nr):
    return 'Chameleon_{0}_{1}'.format(type, nr)

class OpenvasClient(object):
    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
        self.client = metasploit.MSFClient(self.password, username=self.username)

    def load(self):
        def load(self):
            self.client.console_execute('load openvas \n')
            response = self.client.console_read()
            while 'loaded' not in response:
                sleep(10)
                response = self.client.console_read()
            return True

    def connect(self):
        self.client.console_execute('openvas_connect {0} {1} {2} 9390 ok\n'.format(self.username, self.password, self.host))
        response = self.client.console_read()
        while 'successful' not in response:
            sleep(10)
            response = self.client.console_execute()
        return True

    def scan(self, target, audit=3, index=1):
        name = generate_name(index)
        self.client.console_execute('openvas_target_create "{0}" {1} "Chameleon Scan"\n'.format(name, target))
        sleep(3.141) # yes, that's pi
        self.client.console_execute('openvas_task_create {0} "" {1} {2} {3}\n'.format(name, 3, 1)) # fix: clean db
        pass
