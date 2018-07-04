import datetime
import inspect
import json

import SMTPClient

EMAIL_LOGIN_FILENAME = 'secrets/email_client.json'
NOTIFIER_METHOD_NAME_PREFIX = '_Notifier__notify'
TIME_FORMAT = '%I:%M %p %Z'


''' A class for storing addresses to send notifications to those addresses.
'''
class Notifier:
    ''' Creates a Notifier.
    '''
    def __init__(self):
        # notify methods
        allMethods = inspect.getmembers(self, predicate=inspect.ismethod)
        self.__notifierMethods = {}
        prefixLen = len(NOTIFIER_METHOD_NAME_PREFIX)
        for name, method in allMethods:
            if name[:prefixLen] == NOTIFIER_METHOD_NAME_PREFIX:
                self.__notifierMethods[name[prefixLen:]] = method
        # email
        with open(EMAIL_LOGIN_FILENAME, 'r') as f:
            emailInfo = json.load(f)
        self.__emailClient = SMTPClient.SMTPClient(emailInfo['serverAddress'],
                                                   emailInfo['serverPort'],
                                                   emailInfo['userAddress'],
                                                   emailInfo['userPassword'])

    ''' Formats templates.
        @param templates A string or iterable of strings that will be formatted.
        @param timeFormat A datetime.strftime format string to format all datetime objects in **kwargs.
        @param **kwargs Any named argument used to replace strings in every template.
        @return A string or list of strings, depending on the input of template.
    '''
    def __formatTemplates(self, *templates, datetimeFormat=None, **kwargs):
        # fix formatted types (datetime)
        formatMap = {}
        for key, value in kwargs.items():
            if isinstance(value, datetime.datetime):
                formatMap[key] = value.strftime(datetimeFormat)
            else:
                formatMap[key] = value
        # format!
        if isinstance(templates, str):
            return template.format(**formatMap)
        else:
            return tuple(template.format(**formatMap) for template in templates)

    ''' Notifies an address.
        @param method The method to use when notifying the address.
            If null, notify() tries to determine which method to use.
        @param address The address to notify.
        @param head The head of the notification.
        @param body The body of the notification.
        @param **kwargs A mapping of strings to replace in head and body.
    '''
    def notify(self, method, address, head, body, **kwargs):
        if kwargs:
            head, body = self.__formatTemplates(head, body, datetimeFormat=TIME_FORMAT, **kwargs)
        # method
        if method is None:
            try:
                int(address)
                method = 'text'
            except ValueError:
                method = 'email'
        # notify!
        self.__notifierMethods[method](address, head, body)

    ''' Notifies multiple addresses.
        @param methods The methods to use when notifying the address.
            If None or a string, that method is applied to every address.
            If a list, each item in the list is applied to its corresponding address.
        @param addressss The addresses to notify.
        @param head The head of the notification.
        @param body The body of the notification.
        @param **kwargs A mapping of strings to replace in head and body.
    '''
    def notifyMany(self, methods, addresses, head, body, **kwargs):
        if kwargs:
            head, body = self.__formatTemplates(head, body, datetimeFormat=TIME_FORMAT, **kwargs)
        if methods is None or isinstance(methods, str):
            methods = [methods] * len(addresses)
        for method, address in zip(methods, addresses):
            self.notify(method, address, head, body)

    ''' ##### Helper functions:
        These functions are called by notify() to send notifications
        to an address of a particular type.
        For instance, if notify('email', 'address', 'head', 'body') is called,
        __notifyemail('address', 'head', 'body') is called to send the notification.
        
        To add a new notification type to the Notifier class, simply write a new function,
        __notify<notification type>(self, address, head, body), and that method is automatically
        added to the class.
    '''

    def __notifyemail(self, address, head, body):
        self.__emailClient.sendMessage(address, head, body)

    def __notifytext(self, address, head, body):
        self.notify('email', '{}@txt.att.net'.format(address), head, body)
