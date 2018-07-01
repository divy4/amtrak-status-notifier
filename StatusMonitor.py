import datetime
import time

import amtrakwebscraper
import Notifier

HEAD_TEMPLATE_FILENAME = 'teaplates/statusHead.txt'
BODY_TEMPLATE_FILENAME = 'templates/statusBody.txt'

CONFIRM_TIME = datetime.timedelta(minutes=10)
MIN_WAIT = datetime.timedelta(minutes=5)
TIME_FORMAT = ''


class StatusMonitor:
    
    def __init__(self):
        pass

    def __getStatus(self, arrival, trainNumber, station, date):
        print('Scraping status at {}...'.format(datetime.datetime.now()))
        failures = 0
        status = None
        while not status and failures < 5:
            try:
                status = amtrakwebscraper.getStatus(arrival, trainNumber, station, date)
            except StandardError as error:
                failures += 1
                print('Unable to scrape status: {}'.format(error))
                time.sleep(1)
        if failures > 5:
            raise RuntimeError('Failed to scrape status too many times!')
        print('Scraping done!')
        return status

    def __formatTemplate(self, template, **kwargs):
        return template.format(**kwargs)

    def __notify(self, addresses, head, body):
        print('Sending notifications at {}...'.format(datetime.datetime.now()))
        notifier = Notifier.Notifier()
        notifier.notifyMany(None, addresses, head, body)
        print('{} notifications sent!'.format(len(addresses)))

    def __waitForNextNotification(self, expectedTime, minWait):
            diff = expectedTime - datetime.datetime.now()
            delay = max(diff * 0.5, minWait)
            print('Sleeping for {} minutes, {} seconds...'.format(delay.seconds // 60, delay.seconds % 60))
            time.sleep(delay.seconds)
            print('Done!')

    def run(self, trainNumber, station, addresses):
        date = datetime.datetime.now()
        stationCode, stationName, timeZone = amtrakwebscraper.getStationInfo(station)
        # email templates
        with open(HEAD_TEMPLATE_FILENAME, 'r') as f:
            headTemplate = f.read()
        with open(BODY_TEMPLATE_FILENAME, 'r') as f:
            bodyTemplate = f.read()
        status = {'expectedTime': datetime.datetime.max - CONFIRM_TIME}
        while status['expectedTime'] + CONFIRM_TIME > datetime.datetime.now():
            status = self.__getStatus(True, trainNumber, station, date)
            head = self.__formatTemplate(headTemplate, **status)
            body = self.__formatTemplate(bodyTemplate, **status)
            self.__notify(addresses, head, body)
            self.__waitForNextNotification(status['expectedTime'], MIN_WAIT)
        status = self.__getStatus(True, trainNumber, station, date)
        head = self.__formatTemplate(headTemplate, **status)
        body = self.__formatTemplate(bodyTemplate, **status)
        self.__notify(addresses, head, body)
