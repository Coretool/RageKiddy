import http.client
import ssl
import msgpack

class MSFClientError(Exception):
    pass


class MSFClient(object):
    header = {
        'Content-Type': 'binary/message-pack'
    }

    def __init__(self, password, **kwargs):
        self.uri = kwargs.get('uri', '/api/')
        self.port = kwargs.get('port', 55553)
        self.host = kwargs.get('host', '127.0.0.1')
        self.ssl = kwargs.get('ssl', True)
        self.verify = kwargs.get('verify', False)
        self.session = kwargs.get('token')

        if self.ssl:
            if self.verify:
                self.client = http.client.HTTPSConnection(self.host, self.port)
            else:
                self.client = http.client.HTTPSConnection(self.host, self.port,
                                                          context=ssl._create_unverified_context())

        else:
            self.client = http.client.HTTPConnection(self.host, self.port)
        self.login(kwargs.get('username', 'msf'), password)

    def call(self, method, *args):
        """
        Function to call rpc methods
        :param method: rpc method
        :param args: arguments to the rpc method
        :return: result of the rpc method
        """
        data = [method]
        data.extend(args)

        if method == 'auth.login':
            self.client.request('POST', self.uri, msgpack.packb(data), self.header)
            response = self.client.getresponse()

            if response.status == 200:
                return msgpack.unpackb(response.read())
            else:
                raise MSFClientError('Unknown error occurred when trying to login')

        elif self.authenticated:
            data.insert(1, self.sessionid)
            self.client.request('POST', self.uri, msgpack.packb(data), self.header)
            response = self.client.getresponse()

            if (response.status == 200):
                result = msgpack.unpackb(response.read())
                if 'error' in result:
                    raise MSFClientError(result['error_message'])
                return result
            raise MSFClientError('An unknown error occurred')
        else:
            raise MSFClientError('You have to be authenticated')

    def login(self, username, password):
        """
        Logs the user username in
        :param username: user to log in
        :param password: password to log in
        :return:
        """
        response = self.call('auth.login', username, password)
        if response[b'result'] == b'success':
            self.sessionid = response[b'token']
            self.authenticated = True

    def logout(self):
        """
        Logs the current user out
        :return:
        """
        self.call('auth.logout', self.sessionid)
        self.authenticated = False

    def console_create(self):
        """
        Create a new console
        :return:
        """
        return self.call('console.create')

    def console_list(self):
        return self.call('console.list')

    def console_execute(self, command: object, ret: object = False, console: object = '0') -> object:
        print(self.call('console.write', console, command))
        response = self.call('console.read', console)
        if (True == ret):
            return response

    def console_read(self, console=0):
        return str(self.call('console.read', console)[b'data'])
