import json

import SMTPClient

EMAIL_LOGIN_FILENAME = 'secrets/email_client.json'


''' A class for storing addresses to send notifications to those addresses.
'''
class Notifier:
    ''' Creates a Notifier.
    '''
    def __init__(self):
        with open(EMAIL_LOGIN_FILENAME, 'r') as f:
            emailInfo = json.load(f)
        self.__emailClient = SMTPClient.SMTPClient(emailInfo['serverAddress'],
                                                   emailInfo['serverPort'],
                                                   emailInfo['userAddress'],
                                                   emailInfo['userPassword'])

    ''' Notifies an address.
        @param notifType The type of notification the address accepts.
        @param address The address to notify.
        @param head The head of the notification.
        @param body The body of the notification.
    '''
    def notify(self, notifType, address, head, body):
        pass

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
        SMTPClient.sendMessage(address, head, body)
