import requests
import json
import time


def start_nessus(username, password):
    pass


class client(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def build_url(self, resource):
        return '{0}{1}'.format(self.url, resource)

    def call(self, method, resource, data=None):
        headers = {'X-Cookie': 'token={0}'.format(self.token),
                   'content-type': 'application/json'}
        data = json.dumps(data)

        verify = False

        if method == 'POST':
            res = requests.post(self.build_url(resource), data=data, headers=headers, verify=verify)
        elif method == 'PUT':
            res = requests.put(self.build_url(resource), data=data, headers=headers, verify=verify)
        elif method == 'DELETE':
            res = requests.delete(self.build_url(resource), data=data, headers=headers, verify=verify)
        else:
            res = requests.get(self.build_url(resource), params=data, headers=headers, verify=verify)

        if res.status_code != 200:  # error
            pass

        if 'download' in resource:
            return res.content
        else:
            return res.json()

    def login(self):
        """
        Log in to nessus
        """
        data = {'username': self.username, 'password': self.password}
        self.token = self.call('POST', '/session', data=data)['token']

    def logout(self):
        """
        Log out of nessus
        """
        self.call('DELETE', '/session')

    def policies(self):
        """
        Get policies
        """
        res = self.call('GET', '/editor/policy/templates')
        self.policicies = dict((d['title'], d['uuid']) for d in res['templates'])

    def history_id(self, scan):
        """
        Get history id of scan
        """
        res = self.call('GET', '/scans/{0}'.format(scan))
        return dict((h['uuid'], h['history_id']) for h in res['history'])

    def scan_history(self, scan, history):
        """
        Get scan history of scan with history id history
        """
        params = {'history_id': history}
        res = self.call('GET', '/scans/{0}'.format(scan), params)

        return res['info']

    def add(self, name, desc, target, polid):
        """
        Add a scan
        """
        scan = {'uuid': polid,
                'settings': {
                    'name': name,
                    'description': desc,
                    'text_targets': target}
                }
        res = self.call('POST', '/scans', data=scan)

        return res['scan']

    def run(self, scan):
        """
        Run scan
        """
        res = self.call('POST', '/scans/{0}/launch'.format(scan))
        return res['uuid']

    def export_status(self, scan, fid):
        """
        Get export status of a scan
        """
        res = self.call('GET', '/scans/{0}/export/{1}/status'.format(scan, fid))
        return res['status'] == 'ready'

    def export(self, scan, history):
        """
        Export a scan
        """
        data = {'history_id': history, 'format': 'nessus'}
        res = self.call('POST', '/scans/{0}/export'.format(scan), data=data)
        fid = res['file']

        while self.export_status(scan, fid) is False:
            time.sleep(5)

        return fid

    def download(self, scan, fid):
        """
        Download scan
        """
        res = self.call('GET', '/scans/{0}/export/{1}/download'.format(scan, file))
        filename = 'nessus:{0}_{1}'.format(scan, fid)
        with open(filename, 'w') as fi:
            fi.write(res)

            # TODO add cleanup functions
