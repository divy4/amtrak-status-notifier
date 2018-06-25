import datetime
import time

import amtrakwebscraper
import Notifier


BODY_TEMPLATE_FILENAME = 'templates/statusBody.txt'


class StatusMonitor:
    
    def __init__(self):
        pass

    def run(self, trainNumber, station, delay, addresses):
        date = datetime.datetime.now()
        stationCode, stationName = amtrakwebscraper.getStationInfo(station)
        # email templates
        headTemplate = 'Amtrak Status'
        with open(BODY_TEMPLATE_FILENAME, 'r') as f:
            bodyTemplate = f.read()
        # TODO: change loop to stop
        failures = 0
        while True:
            print('Scraping status at {}...'.format(datetime.datetime.now()))
            status = amtrakwebscraper.getStatus(True, trainNumber, stationCode, date)
            if status is None:
                failures += 1
                if failures > 5:
                    raise RuntimeError('Failed too many times!')
                print('Unable to scrape status.')
                print('Sleeping for 5 minutes...')
                time.sleep(60 * 5)
                print('Done!')
                continue
            print('Scraping done!')
            # TODO: make function to format head and body
            head = headTemplate
            body = bodyTemplate.format(difference=status['difference'],
                                       expectedTime=status['expectedTime'],
                                       scheduledTime=status['scheduledTime'],
                                       station=station,
                                       stationCode=stationCode,
                                       stationName=stationName,
                                       trainNumber=trainNumber)
            # notify addresses!
            print('Sending notifications at {}...'.format(datetime.datetime.now()))
            notifier = Notifier.Notifier()
            for address in addresses:
                try:
                    int(address)
                    method = 'text'
                except ValueError:
                    method = 'email'
                notifier.notify(method, address, head, body)
            print('{} notifications sent!'.format(len(addresses)))
            # wait for <delay> minutes
            print('Sleeping for {} minutes...'.format(delay))
            time.sleep(60 * delay)
            print('Done!')
