import os
import sys
import requests
import yaml

from requests import ConnectionError


class Message:
    def __init__(self):
        pass

    @staticmethod
    def debug(message):
        print "[+] %s" % message

    @staticmethod
    def header(message):
        border = "-" * len(message)
        print "\n%s\n%s\n%s\n" % (border, message, border)

    @staticmethod
    def input(question):
        return raw_input("[+] %s" % question)

    @staticmethod
    def success(message):
        print "[+] \x1b[6;30;42m%s\x1b[0m" % message

    @staticmethod
    def error(message):
        print "[+] \x1b[0;30;41m%s\x1b[0m" % message


class CsrfTokenSecurityPolicy:
    header = None

    def __init__(self, header="SET-X-CSRF-TOKEN"):
        self.header = header

    def check(self, request, response):
        count = 0

        if not response.headers.get(self.header):
            Message.error("%s HTTP header is missing" % self.header)

            count += 1

        if request.method.lower() == "post" and response.status_code == 200:
            Message.error("HTTP status code is 200 (yet no CSRF token was sent) and should be 403")

            count += 1

        if count == 0:
            Message.success('CSRF protected')

        return count


class ContentSecurityPolicy:
    header = None

    def __init__(self, header="Content-Security-Policy"):
        self.header = header

    def check(self, request, response):
        count = 0

        if not response.headers.get(self.header):
            Message.error("%s HTTP header is missing" % self.header)

            count += 1

        if count == 0:
            Message.success('Content-Security-Policy protected')

        return count


class Config:
    data = None

    def __init__(self):
        pass

    def from_file(self, file):
        Message.debug("Reading %s" % file)

        with open(file, "r") as file_object:
            Message.debug("Loading %s" % file)

            self.data = yaml.load(file_object.read())

            Message.debug("OpenAPI config file content: %s" % self.data)

            return self.data

    def from_directory(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".yml"):
                config = os.path.join(directory, file)

                answer = Message.input("Is %s the open api config file? [Y/n] " % config)

                if answer is "Y":
                    Message.debug("The %s file was selected as open api config file" % config)

                    return self.from_file(config)
                else:
                    Message.debug("Looking for other *.yml files")

                    continue

        raise Exception("Unable not find *.yml OpenAPI config file in %s" % directory)

    def get_attribute(self, attribute):
        Message.debug("Looking for attribute %s in OpenAPI config" % attribute)

        element = self.data[attribute]

        if element:
            Message.debug("Successfully found attribute %s in OpenAPI config" % attribute)

            return element
        else:
            error = "Unable to find attribute %s in OpenAPI config" % attribute

            Message.debug(error)

            raise Exception(error)

    def get_host(self):
        return self.get_attribute("host")

    def get_paths(self):
        return self.get_attribute("paths")


class Vulnerabilities:
    security_policies = None
    host = None

    def __init__(self, host):
        self.security_policies = [
            CsrfTokenSecurityPolicy,
            ContentSecurityPolicy
        ]
        self.host = host

    def format_url(self, uri):
        url = self.host + uri

        if "http://" not in url:
            url = "http://" + url

        return url

    def identify_vulnerabilities(self, request, response):
        count = 0

        for security_policy in self.security_policies:
            count += security_policy().check(request, response)

        return count

    @staticmethod
    def is_valid_method(method):
        return method.lower() in [
            'get', 'post', 'put', 'patch', 'delete', 'head', 'options'
        ]

    @staticmethod
    def execute_request(method, url):
        Message.debug("[HTTP %s] Testing endpoint [%s] for Security Policies" % (method, url))

        try:
            return requests.request(method, url)
        except ConnectionError:
            Message.debug("The endpoint [%s] to [%s] is not reachable" % (method, url))

            return None

    def from_path(self, method, path):
        url = self.format_url(path)

        Message.debug("Found a new endpoint: [%s] to [%s]" % (method, url))

        if Vulnerabilities.is_valid_method(method):
            response = Vulnerabilities.execute_request(method, url)

            if response is not None:
                return self.identify_vulnerabilities(response.request, response)

        Message.debug("Unable to test the Security Policies against endpoint [%s] to [%s]" % (method, url))

        return 0

    def from_paths(self, paths):
        count = 0

        for path, methods in paths.iteritems():
            for method in methods:
                count += self.from_path(method, path)

        return count


class Application:
    def __init__(self):
        pass

    @staticmethod
    def directory_exists(directory):
        Message.debug("Checking if %s is a valid directory" % directory)

        if os.path.isdir(directory):
            Message.debug("%s is a valid directory" % directory)

            return directory
        else:
            error = "%s is not a valid directory" % directory

            Message.debug(error)

            raise Exception(error)

    @staticmethod
    def select_directory_input():
        return Application.directory_exists(Message.input("Project directory: "))

    @staticmethod
    def select_directory_argv():
        return Application.directory_exists(sys.argv[1])

    @staticmethod
    def get_project_directory():
        if len(sys.argv) == 1:
            return Application.select_directory_input()
        else:
            return Application.select_directory_argv()

    @staticmethod
    def main():
        Message.header("Starting scan")

        directory = Application.get_project_directory()

        config = Config()

        config.from_directory(directory)

        host = config.get_host()

        paths = config.get_paths()

        Message.header("Ready to start scan for: %s" % host)

        vulnerabilities = Vulnerabilities(host)

        count = vulnerabilities.from_paths(paths)

        Message.header("Scan done. Identified %s security vulnerabilities in the web application at [%s]." % (count, host))


if __name__ == "__main__":
    Application.main()
