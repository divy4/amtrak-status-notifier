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
        if not isinstance(serverAddress, str):
            raise TypeError('serverAddress must be a string.')
        elif not isinstance(serverPort, int):
            raise TypeError('serverPort must be an int.')
        elif not isinstance(userAddress, str):
            raise TypeError('userAddress must be a string.')
        elif not isinstance(userPassword, str):
            raise TypeError('userPassword must be a string.')
        self.__server = smtplib.SMTP(serverAddress, serverPort)
        self.__server.ehlo()
        self.__server.starttls()
        self.__server.login(userAddress, userPassword)
        self.__from = userAddress

    ''' Sends an email.
        @param toAddress The email address to send the message to.
        @param subject The subject line.
        @param body The text of the message.
    '''
    def sendMessage(self, toAddress, subject, body):
        if not isinstance(toAddress, str):
            raise TypeError('toAddress must be a string.')
        elif not isinstance(subject, str):
            raise TypeError('subject must be a string.')
        elif not isinstance(body, str):
            raise TypeError('body must be a string.')
        msg = email.mime.multipart.MIMEMultipart()
        msg['From'] = self.__from
        msg['To'] = toAddress
        msg['Subject'] = subject
        msg.attach(email.mime.text.MIMEText(body, 'plain'))
        self.__server.send_message(msg)

if __name__ == '__main__':
    serverAddress = input('Server address: ')
    serverPort = int(input('Server port: '))
    userAddress = input('From address: ')
    userPassword = input('Password: ')
    toAddress = input('To Address: ')

    client = SMTPClient(serverAddress, serverPort, userAddress, userPassword)
    client.sendMessage(toAddress, 'Test', 'This is a test.')
    print('Check the inbox of {}.'.format(toAddress))
