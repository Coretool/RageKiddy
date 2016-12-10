import json
from . import textui
from os import getcwd


def to_bool(string):
    if string.lower() in ('yes', 'true', 't', '1', 'y'):
        return True
    return False


def init():
    print('  ___  _   _    __    __  __  ____  __    ____  _____  _  _ ')
    print(' / __)( )_( )  /__\  (  \/  )( ___)(  )  ( ___)(  _  )( \( )')
    print('( (__  ) _ (  /(__)\  )    (  )__)  )(__  )__)  )(_)(  )  ( ')
    print(' \___)(_) (_)(__)(__)(_/\/\_)(____)(____)(____)(_____)(_)\_)')
    print('by coretool')
    print('\n')

    print('Select mode:\n [1] Scan only\n [2] Scan and exploit\n [3] Sniff network to a PCAP file')
    print(' [4] Credential harvesting from a PCAP file\n [5] MITM\n [6] Fake access point\n [7] Create a honeypot')
    print(
        ' [42] Use a custom mode\n [43] Load a custom mode\n [404] DDOS and other stress test\n [666] Run chameleon in AI mode')
    mode = int(input('Use mode:'))

    {1: setup_scan,
     2: setup_exploit,
     3: setup_sniffer,
     4: setup_harvesting,
     5: setup_mitm,
     6: setup_ap,
     7: setup_honeypot,
     42: setup_custom,
     43: load_custom,
     404: setup_ddos,
     666: setup_ai()}[mode]()


def setup_scan():
    path = getcwd()
    name = raw_input('Workspace name: ')

    print('Select target type:\n [1] Network\n [2] IP range (e.g. 192.168.1.1/255) or single IP (e.g. 192.168.1.2)')
    target_type = int(input('Target type:'))
    target = 'network'
    if target_type == 2:
        target = raw_input('Target [IP or range]:')
    nessus = to_bool(raw_input('Use nessus [y/n]'))
    openvas = to_bool(raw_input('Use openvas [y/n]'))

    config = {'name': name, 'targetType': target_type, 'target': target, 'nessus': nessus, 'openvas': openvas}

    print(textui.scs('mode -> scan\nname -> {0}\ntarget -> {1}\nnessus -> {2}\n openvas -> {3}'))

    file = open(path + '/chameleon.json', 'w')
    file.write(json.dumps(config))


def setup_exploit():
    path = getcwd()
    name = raw_input('Workspace name: ')

    print('Select target type:\n [1] Network\n [2] IP range (e.g. 192.168.1.1/255) or single IP (e.g. 192.168.1.2)')
    target_type = int(input('Target type:'))
    target = 'network'
    if target_type == 2:
        target = raw_input('Target [IP or range]:')
    nessus = to_bool(raw_input('Use nessus [y/n]'))
    openvas = to_bool(raw_input('Use openvas [y/n]'))

    use_single = to_bool(raw_input('Use a single payload like reboot or say [y/n]'))

    config = {'name': name, 'targetType': target_type, 'target': target, 'nessus': nessus, 'openvas': openvas}

    print(textui.scs('mode -> scan\nname -> {0}\ntarget -> {1}\nnessus -> {2}\n openvas -> {3}'))

    file = open(path + '/chameleon.json', 'w')
    file.write(json.dumps(config))


def setup_sniffer():
    pass


def setup_harvesting():
    pass


def setup_mitm():
    pass


def setup_ap():
    pass


def setup_honeypot():
    pass


def setup_custom():
    pass


def load_custom():
    pass


def setup_ddos():
    pass


def setup_ai():
    pass


init()
