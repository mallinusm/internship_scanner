import os
import yaml

from Scanner.Message import Message


class Config:
    data = None

    def __init__(self):
        pass

    """
    Load the OpenAPI config from file.
    """
    def from_file(self, file):
        Message.debug('Reading %s' % file)

        with open(file, 'r') as file_object:
            Message.debug('Loading %s' % file)

            self.data = yaml.load(file_object.read())

            Message.debug('OpenAPI config file content: %s' % self.data)

            return self.data

    """
    Find the OpenAPI config file in a directory and load it.
    """
    def from_directory(self, directory):
        for file in os.listdir(directory):
            if file.endswith('.yml'):
                config = os.path.join(directory, file)

                answer = Message.input('Is %s the open api config file? [Y/n] ' % config)

                if answer is 'Y':
                    Message.debug('The %s file was selected as open api config file' % config)

                    return self.from_file(config)
                else:
                    Message.debug('Looking for other *.yml files')

                    continue

        raise Exception('Unable not find *.yml OpenAPI config file in %s' % directory)

    """
    Get an attribute from the loaded config file.
    """
    def get_attribute(self, attribute):
        Message.debug('Looking for attribute %s in OpenAPI config' % attribute)

        element = self.data[attribute]

        if element:
            Message.debug('Successfully found attribute %s in OpenAPI config' % attribute)

            return element
        else:
            error = 'Unable to find attribute %s in OpenAPI config' % attribute

            Message.debug(error)

            raise Exception(error)

    """
    Retrieve the host (domain) of the web application to test.
    """
    def get_host(self):
        return self.get_attribute('host')

    """
    Retrieve the path of all HTTP endpoints specified to identify security flaws.
    """
    def get_paths(self):
        return self.get_attribute('paths')
