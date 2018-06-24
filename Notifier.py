import SMTPClient


''' A class for storing addresses to send notifications to those addresses.
'''
class Notifier:
    ''' Creates a Notifier.
    '''
    def __init__(self):
        pass

    ''' Adds an address to the notifier.
        @param notifType The method used to notify the address.
        @param address The address to send a notification to.
    '''
    def addAddress(notifType, address):
        pass

    ''' Removes an address from the notifier.
        @param notifType The method used to notify the address.
        @param address The address to send a notification to.
    '''
    def removeAddress(notifType, address):
        pass

    ''' Notifies all addresses.
        @param notifType The type of addresses to notify. If None, all addresses are notified.
        @param head The head of the notification.
        @param body The body of the notification.
    '''
    def notifyAll(notifType, head, body):
        pass

    ''' Notifies an address.
        @param notifType The type of notification the address accepts.
        @param address The address to notify.
        @param head The head of the notification.
        @param body The body of the notification.
    '''
    def notify(notifType, address, head, body):
        pass
