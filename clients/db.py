from subprocess import call
from time import sleep

class DBClient(object):
    def __init__(self, client):
        self.client = client

    def load(self):
        call(['msfdb', 'init'])
        sleep(15)

    def connect(self):
        response = str(self.client.console_execute('db_status')[b'data'])
        while not 'connected' in response:
            sleep(10)
            response = self.client.console_read()
        return True

    def workspace_create(self, name):
        response = str(self.client.console_execute('workspace -a {0}'.format(name))[b'data'])
        while not 'added' in response:
            sleep(3)
            response = self.client.console_read()
        return True

    def workspace_delete(self, name):
        response = str(self.client.console_execute('workspace -d {0}'.format(name))[b'data'])
        while not 'deleted' in response:
            sleep(3)
            response = self.client.console_read()
        return True

    def workspace_select(self, name):
        response = str(self.client.console_execute('workspace {0}'.format(name))[b'data'])
        while not 'Workspace' in response:
            sleep(3)
            response = self.client.console_read()

    def scan_import(self, path):
        response = str(self.client.console_execute('db_import {0}'.format(path))[b'data'])
        while not 'imported' in response:
            sleep(10)
            response = self.client.console_read()

    def scan_export(self, path):
        response = str(self.client.console_execute('db_export -f {0}'.format(path))[b'data'])
        while not 'exported' in response:
            sleep(10)
            response = self.client.console_read

