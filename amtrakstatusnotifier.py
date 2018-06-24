import sys

import Notifier
import StatusMonitor


if __name__ == '__main__':
    # arguments
    if len(sys.argv) < 6:
        print('''Usage: python amtrakstatusnotifier.py <train number> <station> <delay> <admin email> <email 1> [email 2]''')
        sys.exit(0x2fe3)
    trainNumber = int(sys.argv[1])
    station = sys.argv[2]
    delay = int(sys.argv[3])
    adminEmail = sys.argv[4]
    emails = sys.argv[5:]

    try:
        monitor = StatusMonitor.StatusMonitor()
        monitor.run(trainNumber, station, delay, emails)
    except Exception as error:
        message = 'Amtrak Status notifier raised an exception: {}'.format(error)
        # Save to file
        with open('error.log', 'w') as f:
            f.write(message)
        # Send to admin
        notifier = Notifier.Notifier()
        notifier.notify('email', adminEmail, 'Error!', message)
