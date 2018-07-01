import sys

import Notifier
import StatusMonitor


if __name__ == '__main__':
    # arguments
    if len(sys.argv) < 5:
        print('''Usage: python amtrakstatusnotifier.py <train number> <station> <admin email> <email 1> [email 2]''')
        sys.exit(0x2fe3)
    trainNumber = int(sys.argv[1])
    station = sys.argv[2]
    adminAddress = sys.argv[3]
    addresses = sys.argv[4:]
    # Monitor
    try:
        monitor = StatusMonitor.StatusMonitor()
        monitor.run(trainNumber, station, addresses)
    except Exception as error:
        message = 'Amtrak Status notifier raised an exception: {}'.format(error)
        # Save to file
        with open('error.log', 'w') as f:
            f.write(message)
        # Send to admin
        notifier = Notifier.Notifier()
        try:
            int(adminAddress)
            method = 'text'
        except ValueError:
            method = 'email'
        notifier.notify(method, adminAddress, 'Error!', message)
