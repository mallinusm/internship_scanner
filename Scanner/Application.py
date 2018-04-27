import argparse

from Scanner.Message import Message
from Scanner.PoliciesTester import PoliciesTester


class Application:
    def __init__(self):
        pass

    @staticmethod
    def start():
        parser = argparse.ArgumentParser(description='Scan a SeCloud web application for security vulnerabilities.')
        parser.add_argument('--delay', metavar='Delay', type=int, nargs='?',
                            help='The delay in seconds when sending web requests.')
        parser.add_argument('path', metavar='Path', type=str, nargs='?', help='Path to the SeCloud project')

        try:
            PoliciesTester(parser.parse_args()).scan()
        except KeyboardInterrupt:
            pass
        except EOFError:
            pass
        except Exception, exception:
            Message.debug('Application error: %s' % exception.message)


if __name__ == '__main__':
    Message.info('The application was started without Makefile')
    Message.info('You can start the application using the command "make run"')
    Application.start()
