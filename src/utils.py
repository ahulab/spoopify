import datetime
import inspect
import os

class Logger:
    def __init__(self, **kwargs):
        if not kwargs['caller_filepath']:
            raise ValueError('caller_filepath must be included')

        caller_filename = kwargs['caller_filepath'].split('/')[-1]
        if kwargs.get('clazz') == None:
            self.prefix = caller_filename
        elif inspect.isclass(kwargs['clazz']):
            self.prefix = f"{caller_filename} - {kwargs['clazz'].__name__}" 
        else:
            raise ValueError("clazz var is invalid")

        self.levels = {
            'INFO': os.getenv('INFO', True) == True,
            'DEBUG': os.getenv('DEBUG', False) == True
        }

    def log(self, message):
        print('{} {}: {}'.format(datetime.datetime.now().time(), self.prefix, message))
    
    def info(self, message):
        if self.levels['INFO']:
            self.log(message)

    def debug(self, message):
        if self.levels['DEBUG']:
            self.log(message)
