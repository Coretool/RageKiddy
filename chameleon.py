import sys
sys.path.append('./')
import metasploit
import nessus
import random

# hook up to cli frontend and config backend

username = ''
password = ''
target = ''
workspace_name = ''
#TODO add service starters

# metasploit setup
mclient = metasploit.rpcclient.MSFClient(password, username=username)
mclient.console_create()




