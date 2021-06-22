from datetime import datetime
import os
from random import randrange


def generateLogs(directory,date):
    timestamp = int(datetime.timestamp(date))
    print(timestamp)

    if not os.path.exists(directory):
        print("Creating directory..")
        os.mkdir(directory)

    # for _ in range(1440):
    #
    #     cpu_usage = randrange(0,100)

if __name__ == "__main__":
    today = datetime.now().now().replace(hour=0, minute=0, second=0, microsecond=0)
    directory = 'data'
    generateLogs(directory, today)