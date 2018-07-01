import datetime
import time

import amtrakwebscraper
import Notifier

HEAD_TEMPLATE_FILENAME = 'templates/statusHead.txt'
BODY_TEMPLATE_FILENAME = 'templates/statusBody.txt'

CONFIRM_TIME = datetime.timedelta(minutes=10)
MIN_WAIT = datetime.timedelta(minutes=5)
TIME_FORMAT = '%I:%M %p %Z'


class StatusMonitor:
    
    def __init__(self):
        pass

    def __now(self):
        return datetime.datetime.now(datetime.timezone.utc)

    def __getStatus(self, arrival, trainNumber, station, date):
        print('Scraping status at {}...'.format(self.__now()))
        failures = 0
        status = None
        while not status and failures < 5:
            try:
                status = amtrakwebscraper.getStatus(arrival, trainNumber, station, date)
            except Exception as error:
                failures += 1
                print('Unable to scrape status: {}'.format(error))
                time.sleep(1)
        if failures > 5:
            raise RuntimeError('Failed to scrape status too many times!')
        print('Scraping done!')
        return status

    def __notify(self, addresses, headTemplate, bodyTemplate, status):
        print('Sending notifications at {}...'.format(self.__now()))
        notifier = Notifier.Notifier()
        notifier.notifyMany(None, addresses, headTemplate, bodyTemplate, **status)
        print('{} notifications sent!'.format(len(addresses)))

    def __waitForNextNotification(self, expectedTime, minWait):
        diff = expectedTime - self.__now()
        delay = max(diff * 0.5, minWait)
        print('Sleeping for {} minutes, {} seconds...'.format(delay.seconds // 60,
                                                              delay.seconds % 60))
        time.sleep(delay.seconds)
        print('Done!')

    def run(self, trainNumber, station, addresses):
        date = self.__now()
        stationCode, stationName, timeZone = amtrakwebscraper.getStationInfo(station)
        # email templates
        with open(HEAD_TEMPLATE_FILENAME, 'r') as f:
            headTemplate = f.read()
        with open(BODY_TEMPLATE_FILENAME, 'r') as f:
            bodyTemplate = f.read()
        # loop!
        status = self.__getStatus(True, trainNumber, station, date)
        while status['expectedTime'] + CONFIRM_TIME > self.__now():           
            self.__notify(addresses, headTemplate, bodyTemplate, status)
            self.__waitForNextNotification(status['expectedTime'], MIN_WAIT)
            status = self.__getStatus(True, trainNumber, station, date)
        self.__notify(addresses, headTemplate, bodyTemplate, status)
