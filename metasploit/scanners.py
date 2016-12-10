from uuid import getnode
import socket
import re


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]


def arp_sweep(client, threads=8, rhosts='192.168.1.1-255'):
    """
    This function runs the arp_sweep auxiliary and returns the ips of the hosts that are up
    :param rhosts: targets
    :param client: a MSFRPC client
    :param threads: num of threads to run on
    :return: list of ips
    """
    mac = ':'.join(("%012X" % getnode())[i:i + 2] for i in range(0, 12, 2))
    ip = get_ip()
    client.console_execute('use auxiliary/scanner/discovery/arp_sweep \n')
    client.console_execute('set RHOSTS ' + rhosts + '\n')
    client.console_execute('set SHOST ' + ip + '\n')
    client.console_execute('set SMAC ' + mac + '\n')
    client.console_execute('set THREADS ' + str(threads) + '\n')
    result = str(client.console_execute('run' + '\n', True)[b'data'])
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', result)
    client.console_execute('back')
    return ips


def nmap_scan(client, target):
    """
    Runs an nmap scan with os detection
    :param client: MSFRPC client
    :param target: target host
    :return: os and services
    """
    client.console_execute('sudo db_nmap -A ' + target, True)


def nessus_scan(client, path):
    """
    Imports a nessus scan
    :param client: MSFRPC client
    :param path: path to scan
    :return:
    """
    client.console_execute('db_import {0}'.format(path))


def host_table(client):
    """

    :param client: MSFRPC client
    :return: all scanned host with their arch, mac, hostname, os and info
    """
    hosts = []

    addresses = client.console_execute('hosts -c address \n', True)
    print(addresses)
    addresses = str(addresses[b'data'])
    addresses = addresses.split('\n')

    arch = str(client.console_execute('hosts -c address,arch \n', True)[b'data'])
    arch = arch.split('\n')
    for line in arch:
        for address in addresses:
            if address in line:
                line = ' '.join(line.split())
                line = line.split(' ')  # 0 : ip, 1 : arch
                if len(line) == 2:
                    hosts.append({'ip': address, arch: line[1]})
                else:
                    hosts.append({'ip': address})

    mac = str(client.console_execute('hosts -c address,mac \n', True)[b'data'])
    mac = mac.split('\n')
    for line in mac:
        for host in hosts:
            if host.ip in line:
                line = ' '.join(line.split())
                line = line.split(' ')
                if len(line) == 2:
                    host.mac = line[1]
                else:
                    host.mac = None

    name = str(client.console_execute('hosts -c address,name \n', True)[b'data'])
    name = name.split('\n')
    for line in name:
        for host in hosts:
            if host.ip in line:
                line = ' '.join(line.split())
                line = line.split(' ')
                if len(line) == 2:
                    host.name = line[1]
                else:
                    host.name = None

    os = str(client.console_execute('hosts -c address,os_flavour \n', True)[b'data'])
    os = os.split('\n')
    for line in os:
        for host in hosts:
            if host.ip in line:
                line = ' '.join(line.split())
                line = line.split(' ')
                if len(line) == 2:
                    host.os = line[1]
                else:
                    host.os = None

    infos = str(client.console_execute('hosts -c address, info \n', True)[b'data'])
    infos = infos.split('\n')
    for info in infos:
        for host in hosts:
            if host.ip in info:
                info = ' '.join(info.split())
                info = info.split(' ')
                if len(info) == 2:
                    host.info = info
                else:
                    host.info = None
    return hosts
