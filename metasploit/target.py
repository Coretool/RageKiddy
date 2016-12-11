"""
All Target related code goes here.
 -> service handling
 -> vulnerability handling
 -> exploit addition
"""
import sys
import re
sys.path.append('./')
from exploits import Exploit


class Target(object):
    """
    Target class
    All targets selected will have their own object containing the data specified in __init__().
    """
    def __init__(self, host):
        self.arch = host.arch
        self.ip = host.ip
        self.mac = host.mac
        self.os = host.os
        self.services = []
        self.exploits = []
        self.vulns = []

    def add_services(self, client):
        """
        Returns all services for host
        :param client: MSFRPC client
        :return: services on host (name, port and info)
        """
        table = []
        services = str(client.console_execute('services -c name {0}\n'.format(self.ip), True)[b'data'])
        services = services.split('\n')
        for service in services:
            service = ' '.join(service.split())
            service = service.split(' ')
            if service[0] == self.ip:
                table.append({'name': service[1]})

        ports = str(client.console_execute('services -c name,port {0}\n '.format(self.ip), True)[b'data'])
        ports = ports.split('\n')
        for port in ports:
            for service in table:
                if service.name in port:
                    port = ' '.join(port.split())
                    port = port.split(' ')  # 0 : host, 1 : name, 2 : port
                    if len(port) == 3:
                        service.port = port[2]

        infos = str(client.console_execute('services -c name,info {0}\n '.format(self.ip), True)[b'data'])
        infos = infos.split('\n')
        for info in infos:
            for service in table:
                if service.name in infos:
                    info = ' '.join(info.split())
                    info = info.split(' ')
                    if len(info) == 3:
                        service.info = info[2]

        self.services = table

    def add_vulns(self, client):
        """
        Add vulnerabilites to the target
        :param client: MSFRPC client
        :return:
        """
        res = ''
        for port in self.services:
            res += str(client.console_execute('vulns -p {0}\n'.format(port.port))[b'data'])

        res = res.split('\n')
        for line in res:
            if self.ip in line:
                # Time: 2010-09-28 01:51:38 UTC Vuln: host=192.168.1.161 port=445 proto=tcp name=NSS-10860 refs=CVE-2000-1200,BID-959,OSVDB-714
                port = re.findall(r'port=[0-9]*', line) 
                name = re.findall(r'name=[0-9aA-zZ\-]', line)
                refs = re.findall(r'refs=[0-9aA-zZ\-,]', line)
                self.vulns.append({'name': name, 'refs': refs, 'port': port})

    def resolve_vuln(self, client, vuln):
        """
        Search for an exploit
        :param client: MSFRPC client
        :param vuln: a vulnerability string
        :return:
        """
        refs = vuln.refs

        if ',' in refs:
            refs = refs.split(',')
            for ref in refs:
                if 'cve' in str.lower(ref):  # CVE-2008-0166
                    cve = ref.split('-')[1] + '-' + ref.split('-')[2]
                    res = str(client.console_execute('search cve:{0}\n'.format(cve))[b'data'])
                    res = self.read_search(res)
                    self.exploits.append(Exploit(res.name, self.os, vuln.port, self.ip))

    def read_search(self, search):
        """
        Read search examples line by line
        :param search: a raw text string containing the search results
        :return: array with the names (paths) of the exploits
        """
        results = []
        search = search.split('\n')
        for result in search:
            if 'exploit' in result:
                result = ' '.join(result.split())
                result = result.split(' ')  # 0 : name, 1 : date, 2 : rank, 3 : description
                results.append(result[0])
        return results
