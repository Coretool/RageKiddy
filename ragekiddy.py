import sys
import uuid
sys.path.append('./')
import clients
from colors import *
import lib

LOG_LEVEL = 0  # silent
# CHAMELEON_ENABLED = True

print(' ____    __    ___  ____  _  _  ____  ____  ____  _  _ ')
print('(  _ \  /__\  / __)( ___)( )/ )(_  _)(  _ \(  _ \( \/ )')
print(' )   / /(__)\( (_-. )__)  )  (  _)(_  )(_) ))(_) )\  / ')
print('(_)\_)(__)(__)\___/(____)(_)\_)(____)(____/(____/ (__) ')
print('by coretool')
print('\n')


print(mrk('Input a target for RageKiddy. You can select a single ip like 192.168.1.1'))
print(mrk('a subnetwork like 192.168.1.1/6 or the complete network (192.168.1.1/255)'))
target = input('')

debug('Generating username and password')
username = str(uuid.uuid4())
password = str(uuid.uuid4())

debug(username)
debug(password)

# TODO add service starters for all external tools

info('Creating metasploit client')
mclient = clients.metasploit.MSFClient(password, username=username)  # metasploit client
mclient.login()
mclient.console_create()

info('Creating nessus client')
nsclient = clients.nessus.NessusClient(username, password, mclient)  # nessus client
info('Attempting to connect to the nessus daemon...')
status = nsclient.load()
if status == False:
    error('Nessus connection failed')
else:
    status = nsclient.connect
    if status == False:
        error('Nessus connection failed')
        nsclient = None
    else:
        info('Done')

info('Creating nexpose client')
nxclient = clients.nexpose.NexposeClient(username, password, mclient)  # nexpose client
info('Attempting to connect to the nexpose daemon...')
status = nxclient.load()
if status == False:
    error('Nexpose connection failed')
else:
    status = nxclient.connect
    if status == False:
        error('Nexpose connection failed')
        nxclient = None
    else:
        info('Done')

info('Creating openvas client')
oclient = clients.openvas.OpenvasClient(username, password, mclient)  # openvas client
info('Attempting to connect to the openvas daemon...')
status = oclient.load()
if status == False:
    error('Openvas connection failed')
else:
    status = oclient.connect
    if status == False:
        error('Openvas connection failed')
        oclient = None
    else:
        info('Done')

info('Running nessus scan...')
if nsclient:
    status = nsclient.scan(target)
    if status == False:
        error('Nessus scan timeout')
    else:
        info('Done')

info('Running nexpose scan...')
if nxclient:
    status = nxclient.scan(target)
    if status == False:
        error('Nexpose scan timeout')
    else:
        info('Done')

info('Running openvas scan...')
if oclient:
    status = oclient.scan(target)
    if status == False:
        error('Openvas scan timeout')
    else:
        info('Done')

hosts = []
for host in lib.host_table(mclient):
    hosts.append(lib.Target(mclient, host.ip, host.mac))

for host in hosts:
    host.add_services()
    host.add_vulns()
    host.resolve_vulns()

for host in hosts:
    if len(host.exploits) > 0:
        for exploit in host.exploits:
            lib.select_exploit(exploit)
            lib.select_target(host.ip)
            payloads = lib.get_payloads()
            if 'linux' in host.os_name or 'linux' in host.os_flavor:

                """ TODO add chameleon support
                if CHAMELEON_ENABLED == True:
                    pass
                """

            elif 'osx' in host.os_name or 'osx' in host.os_flavor:
                pass
            elif 'windows' in host.os_name or 'windows' in host.os_flavor:
                pass
            else:
                pass