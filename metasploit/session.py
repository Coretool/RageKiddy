class Session(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def connect(self, client):
        client.console_execute('session -i {0}'.format(self.id))

    def execute(self, client, command):
        client.console_execute(command + '\n')

    def execute_return(self, client, command):
        return str(client.console_execute(command + '\n')[b'data'])
