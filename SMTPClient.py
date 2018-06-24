import email.mime.multipart
import email.mime.text
import smtplib


''' A class for basic SMTP server connection.
'''
class SMTPClient:
    ''' Creates a new SMTPClient.
        @param serverAddress The SMTP server address.
        @param serverPort The SMTP server port.
        @param userAddress The user's email address to send emails from.
        @param userPassword The password to userAddress's account.
    '''
    def __init__(self, serverAddress, serverPort, userAddress, userPassword):
        pass

    ''' Sends an email.
        @param toAddress The email address to send the message to.
        @param subject The subject line.
        @param body The text of the message.
    '''
    def sendMessage(self, toAddress, subject, body):
        pass
