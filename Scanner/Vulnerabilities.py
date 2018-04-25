import time
import os

import requests
from requests import ConnectionError

from Scanner.Message import Message


class Vulnerabilities:
    security_policies = None
    host = None

    def __init__(self, host):
        self.load_security_policies()

        self.host = host

    def load_security_policies(self):
        path = os.path.join(os.getcwd(), 'policies')

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.sp')]

        self.security_policies = []

        for f in files:
            self.security_policies.append(os.path.join(path, f))

    def format_url(self, uri):
        url = self.host + uri

        if 'http://' not in url:
            url = 'http://' + url

        return url

    def identify_vulnerabilities(self, request, response):
        count = 0

        locals = {
            'count': count,
            'request': request,
            'response': response
        }

        for security_policy in self.security_policies:
            Message.debug('Security policy: %s' % security_policy)

            try:
                execfile(security_policy, dict(), locals)
                count += (locals['count'] - count)
            except Exception, exception:
                Message.debug(exception.message)

        return count

    @staticmethod
    def is_valid_method(method):
        return method.lower() in [
            'get', 'post', 'put', 'patch', 'delete', 'head', 'options'
        ]

    @staticmethod
    def execute_request(method, url):
        Message.debug('[HTTP %s] Testing endpoint [%s] for Security Policies' % (method, url))

        try:
            return requests.request(method, url)
        except ConnectionError:
            Message.debug('The endpoint [%s] to [%s] is not reachable' % (method, url))

            return None

    def from_path(self, method, path):
        url = self.format_url(path)

        Message.debug('Found a new endpoint: [%s] to [%s]' % (method, url))

        if Vulnerabilities.is_valid_method(method):
            response = Vulnerabilities.execute_request(method, url)

            if response is not None:
                return self.identify_vulnerabilities(response.request, response)

        Message.debug('Unable to test the Security Policies against endpoint [%s] to [%s]' % (method, url))

        return 0

    def from_paths(self, paths, delay=None):
        count = 0

        for path, methods in paths.iteritems():
            for method in methods:
                count += self.from_path(method, path)

                if delay is not None:
                    Message.debug('Waiting for a delay of %s second' % delay)
                    time.sleep(delay)

        return count
