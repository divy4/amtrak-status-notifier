import SMTPClient


''' A class for storing addresses to send notifications to those addresses.
'''
class Notifier:
    ''' Creates a Notifier.
    '''
    def __init__(self):
        pass

    ''' Notifies an address.
        @param notifType The type of notification the address accepts.
        @param address The address to notify.
        @param head The head of the notification.
        @param body The body of the notification.
    '''
    def notify(self, notifType, address, head, body):
        pass
