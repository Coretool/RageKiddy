import sys
sys.path.append('./')
import rpcclient, scanners

# create a new msfrpc client
client = rpcclient.MSFClient('password', username='user')
# create a new console
client.console_create()

print(client.call('module.compatible_payloads' ,'linux/mysql/mysql_yassl_getname'))
