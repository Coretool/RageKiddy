from time import sleep
from . import metasploit

class NexposeClient(object):
    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
        self.client = metasploit.MSFClient(self.password, username=self.username)

    def load(self):
        """
        Load nexpose integration
        :return:
        """
        self.client.console_execute('load nexpose\n')
        response = self.client.console_read()
        while 'loaded' not in response:
            sleep(10)
            response = self.client.console_read()
        return True

    def connect(self):
        """
        Connect to nexpose server
        :return:
        """
        self.client.console_execute('nexpose_connect {0}:{1}@{2} ok\n'.format(self.username, self.password, self.host))
        response = self.client.console_read()
        while 'Authenticated' not in response:
            sleep(10)
            response = self.client.console_read()
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
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
        return True

    # non-required nexpose-only functions

    def discover(self, range='192.168.1.1/255'):
        self.client.console_execute('nexpose_discover {0} \n'.format(range))
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
        return True

    def dos(self, range='192.168.1.1/255'):
        self.client.console_execute('nexpose_dos {0} \n'.format(range))
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
        return True

    def exhaustive(self, range='192.168.1.1/255'):
        self.client.console_execute('nexpose_exhaustive {0} \n'.format(range))
        while 'Completed' not in response:
            sleep(10)
            response = self.client.console_read()
        return True