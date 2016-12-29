import sys
from time import sleep
sys.path.append('./')

class NexposeClient(object):
    def __init__(self, username, password, client, host):
        self.username = username
        self.password = password
        self.host = host
        self.client = client

    def load(self):
        """
        Load nexpose integration
        :return:
        """
        self.client.console_execute('load nexpose\n')
        response = self.client.console_read()
        i = 0
        while 'loaded' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else :
                i += 1
        return True

    def connect(self):
        """
        Connect to nexpose server
        :return:
        """
        self.client.console_execute('nexpose_connect {0}:{1}@{2} ok\n'.format(self.username, self.password, self.host))
        response = self.client.console_read()
        i = 0
        while 'Authenticated' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else :
                i += 1
        return True

    def scan(self, target, audit='full-audit'):
        """
        Perform nexpose scan (defaulting to full-audit)
        :param target:
        :param audit:
        :return:
        """
        self.client.console_execute('nexpose_scan -t {0} {1}\n'.format(audit, target))
        response = self.client.console_read()
        i = 0
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else :
                i += 1
        return True

    # nexpose-only functions

    def discover(self, range='192.168.1.1/255'):
        self.client.console_execute('nexpose_discover {0} \n'.format(range))
        i = 0
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else :
                i += 1
        return True

    def dos(self, range='192.168.1.1/255'):
        self.client.console_execute('nexpose_dos {0} \n'.format(range))
        i = 0
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else :
                i += 1
        return True

    def exhaustive(self, range='192.168.1.1/255'):
        self.client.console_execute('nexpose_exhaustive {0} \n'.format(range))
        i = 0
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else :
                i += 1
        return True
