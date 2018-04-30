import os

from Scanner.Config import Config
from Scanner.Message import Message
from Scanner.Vulnerabilities import Vulnerabilities


class PoliciesTester:
    arguments = None

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def directory_exists(directory):
        Message.debug('Checking if %s is a valid directory' % directory)

        if os.path.isdir(directory):
            Message.debug('%s is a valid directory' % directory)

            return directory
        else:
            raise Exception('%s is not a valid directory' % directory)

    @staticmethod
    def select_directory_input():
        return PoliciesTester.directory_exists(Message.input('Project directory: '))

    def get_project_directory(self):
        directory = self.arguments.path

        if directory:
            return PoliciesTester.directory_exists(directory)
        else:
            return PoliciesTester.select_directory_input()

    """
    Execute a full scan (test all security policies) against a web application.
    """
    def scan(self):
        Message.header('Starting scan')

        directory = self.get_project_directory()

        config = Config()

        config.from_directory(directory)

        host = config.get_host()

        paths = config.get_paths()

        Message.header('Ready to start scan for the web application at %s' % host)

        vulnerabilities = Vulnerabilities(host)

        count = vulnerabilities.from_paths(paths, self.arguments.delay)

        Message.header(
            'Scan done. Identified %s potential security flaws in the web application at [%s]' % (count, host)
        )
