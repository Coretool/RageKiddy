class Session(object):
    def __init__(client, job):
        infos = client.call('job.info', job)
        exploit = str(infos[b'name']).replace('Exploit:','')
        sessions = client.call('session.list')
        for session in sessions:
            if exploit in str(sessions[session][b'via_exploit'])
            self.id = str(session)
            self.type = str(sessions[session][b'type'])
            break
        
    def write(self, client, command):
        """
        Write to a session
        """
        if 'meterpreter' in self.type:
            client.call('session.meterpreter_write', self.id, command + '\n')
        else:
            client.call('session.shell_write', self.id, command + '\n')
            
    def read(self, client):
        """
        Read from a session
        """
        if 'meterpreter' in self.type:
            return client.call('session.meterpreter_read', self.id)[b'result']
        else:
            return client.call('session.shell_read', self.id)[b'result']
        
    def getsystem(self, client):
        """
        Try to raise to SYSTEM level on windows (needs meterpreter)
        """
        self.write(client, 'use priv\n')
        self.write(client, 'getsystem')
        self.write(client, 'getuid')
        if 'SYSTEM' in str(self.read(client)):
            return True
        return False
    
    def raise():
        pass

    def gather():
        pass

    def interactive(self, client):
        """
        Run a interactive shell
        """
        print('Entering interactive session of type {0}'.format(self.type))
        while True:
            command = raw_input('>')
            # TODO add specific chameleon commands
            if str.lower(command) == 'exit_interactive':
                break
            self.write(client, command)
            print(self.read(client))
            
        print('Exiting interactive session')
        return False
