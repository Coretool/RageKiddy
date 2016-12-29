import sys
from time import sleep
sys.path.append('./')

def generate_name(type, nr):
    return 'Chameleon_{0}_{1}'.format(type, nr)

class NessusClient(object):
    def __init__(self, username, password, client, host = '127.0.0.1'):
        self.username = username
        self.password = password
        self.host = host
        self.client = client # MSFRPC client

    def load(self):
        self.client.console_execute('load nessus \n')
        response = self.client.console_read()
        i = 0
        while 'loaded' not in response:
            sleep(10)
            response = self.client.console_read()
            if i == 100:
                return False
            else:
                i += 1
        return True

    def connect(self):
        self.client.console_execute('nessus_connect {0}:{1}@{2} ok\n'.format(self.username, self.password, self.host))
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

    def scan(self, target, policy=1, index=1):
        name = generate_name(index)
        self.client.console_execute('nessus_scan_new {0} {1} {2}'.format(policy, name, target))
        response = str(self.client.console_execute('nessus_report_list \n')[b'data'])
        i = 0
        while name not in response:
            sleep(10)
            response = str(self.client.console_execute('nessus_report_list \n')[b'data'])
            if i == 100:
                return False
            else :
                i += 1
        lines = response.split('\n')
        for line in lines:
            if name in line:
                line = line.split(' ')
                self.client.console_execute('nessus_report_get {0} \n'.format(line[0]))
        return True
