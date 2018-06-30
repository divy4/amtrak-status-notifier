import datetime
import time

import amtrakwebscraper
import Notifier


BODY_TEMPLATE_FILENAME = 'templates/statusBody.txt'
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

    def __waitForNextNotification(self, delay):
            print('Sleeping for {} minutes...'.format(delay))
            time.sleep(60 * delay)
            print('Done!')

    def run(self, trainNumber, station, delay, addresses):
        date = datetime.datetime.now()
        stationCode, stationName, timeZone = amtrakwebscraper.getStationInfo(station)
        # email templates
        headTemplate = 'Amtrak Status'
        with open(BODY_TEMPLATE_FILENAME, 'r') as f:
            bodyTemplate = f.read()
        # TODO: change loop to stop
        failures = 0
        while True:
            status = self.__getStatus(True, trainNumber, station, date)
            status['stationCode'] = stationCode
            status['stationName'] = stationName
            status['trainNumber'] = trainNumber
            head = self.__formatTemplate(headTemplate, **status)
            body = self.__formatTemplate(bodyTemplate, **status)
            self.__notify(addresses, head, body)
            self.__waitForNextNotification(delay)
