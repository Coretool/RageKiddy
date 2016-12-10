import sys
sys.path.append('./')
import rpcclient, scanners

# create a new msfrpc client
client = rpcclient.MSFClient('secret', username='user')
# create a new console
client.console_create()

scanners.nmap_scan(client, '192.168.1.101')
print(scanners.host_table(client))
