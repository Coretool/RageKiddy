import sys 
sys.path.append('./')
import metasploit
from time import sleep

class NmapClient(object):
    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
        self.client = metasploit.MSFClient(self.password, username=self.username)

    def load(self):
        response = str(self.client.console_execute('db_status\n')[b'data'])
        if 'connected' in response:
            return True
        else:
            return False

    def scan(self, target, parameter='A'):
        self.client.console_execute('db_nmap -{0} {1}\n'.format(parameter, target))
        response = self.client.console_read()
        while 'done' not in response:
            sleep(10)
            respone = self.client.console_read()
        return True
        
    

