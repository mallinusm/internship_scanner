class Message:
    def __init__(self):
        pass

    @staticmethod
    def debug(message):
        print '[+] %s' % message

    @staticmethod
    def header(message):
        border = '-' * len(message)
        print '\n%s\n%s\n%s\n' % (border, message, border)

    @staticmethod
    def input(question):
        return raw_input('[+] %s' % question)

    @staticmethod
    def success(message):
        print '[+] \x1b[6;30;42m%s\x1b[0m' % message

    @staticmethod
    def error(message):
        print '[+] \x1b[0;30;41m%s\x1b[0m' % message

    @staticmethod
    def info(message):
        print '[+] \x1b[0;30;44m%s\x1b[0m' % message
