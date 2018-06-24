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
