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

    """
    Load the filename of security policies (*.sp files inside /policies).
    """
    def load_security_policies(self):
        path = os.path.join(os.getcwd(), 'policies')

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.sp')]

        self.security_policies = []

        for f in files:
            self.security_policies.append(os.path.join(path, f))

    """
    Make sure an url starts with the "http://" prefix.
    """
    def format_url(self, uri):
        url = self.host + uri

        if 'http://' not in url:
            url = 'http://' + url

        return url

    """
    Identify security flaws by testing the security policies on the HTTP request and response.
    """
    def identify_vulnerabilities(self, request, response):
        count = 0

        variables = {
            'count': count,
            'request': request,
            'response': response,
            'Message': Message
        }

        for security_policy in self.security_policies:
            Message.debug('Security policy: %s' % security_policy)

            try:
                execfile(security_policy, dict(), variables)
                count += (variables['count'] - count)
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

    """
    Execute a HTTP request for the method and path.
    """
    def from_path(self, method, path):
        url = self.format_url(path)

        Message.debug('Found a new endpoint: [%s] to [%s]' % (method, url))

        if Vulnerabilities.is_valid_method(method):
            response = Vulnerabilities.execute_request(method, url)

            if response is not None:
                return self.identify_vulnerabilities(response.request, response)

        Message.debug('Unable to test the Security Policies against endpoint [%s] to [%s]' % (method, url))

        return 0

    """
    Execute HTTP requests for the methods and paths.
    """
    def from_paths(self, paths, delay=None):
        count = 0

        for path, methods in paths.iteritems():
            for method in methods:
                count += self.from_path(method, path)

                if delay is not None:
                    Message.debug('Waiting for a delay of %s second' % delay)
                    time.sleep(delay)

        return count
