import datetime
import time

import amtrakwebscraper
import Notifier


BODY_TEMPLATE_FILENAME = 'templates/statusBody.txt'


class StatusMonitor:
    
    def __init__(self):
        pass

    def run(self, trainNumber, station, delay, emails):
        date = datetime.datetime.now()
        stationCode, stationName = amtrakwebscraper.getStationInfo(station)
        # email templates
        headTemplate = 'Amtrak Status'
        with open(BODY_TEMPLATE_FILENAME, 'r') as f:
            bodyTemplate = f.read()
        # TODO: change loop to stop
        while True:
            status = amtrakwebscraper.getStatus(True, trainNumber, stationCode, date)
            # TODO: make function to format head and body
            head = headTemplate
            body = bodyTemplate.format(difference=status['difference'],
                                       expectedTime=status['expectedTime'],
                                       scheduledTime=status['scheduledTime'],
                                       station=station,
                                       stationCode=stationCode,
                                       stationName=stationName,
                                       trainNumber=trainNumber)
            # notify emails!
            notifier = Notifier.Notifier()
            for email in emails:
                notifier.notify('email', email, head, body)
            # wait for <delay> minutes
            time.sleep(60 * delay)
