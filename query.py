import sys
import os
import datetime

def checkDateFormat(date,error_at):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        print("Incorrect date format at "+error_at+", should be YYYY-MM-DD")
        return False

def checkTimeFormat(time,error_at):
    try:
        datetime.datetime.strptime(time,"%H:%M")
        return True
    except ValueError:
        print("Incorrect time format at "+error_at+", should be HH:MM")
        return False


def getQuery(DATA_PATH):
    while True:
        command = input('>')
        if str.lower(command) == 'exit':
            break

        words = command.split(' ')
        if str.lower(words[0]) != 'query' or len(words) != 7:
            print('Query syntax: QUERY IP cpu_id time_start time_end')
            print('Example: QUERY 192.168.1.10 1 2014-10-31 00:00 2014-10-31 00:05')
            print("Enter 'EXIT' to stop.")
            continue

        ip = words[1]
        if len([s for s in ip.split('.') if s.isdigit()]) != 4:
            print('Incorrect IPv4 address entered.')
            continue

        cpu_id = words[2]
        if not cpu_id.isdigit():
            print('Incorrect CPU ID entered.')
            continue

        # check date time format
        start_date = words[3]
        start_time = words[4]
        end_date = words[5]
        end_time = words[6]

        if not checkDateFormat(start_date,'start_date') or not checkTimeFormat(start_time,'start_time'):
            continue

        if not checkDateFormat(end_date,'end_date') or not checkTimeFormat(end_time,'end_time'):
            continue

        start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")

        timestamps = []
        no_days = int((end_date - start_date).days)+1
        print(no_days)
        for i in range(no_days):
            timestamps.append(int(datetime.datetime.timestamp(start_date+ datetime.timedelta(days=i))))

        print(timestamps)

        # check if directory exists
        # check if csv exists
        # read csv




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give path to directory.')
        print('Usage: python query.py [Path to Directory]')
        exit(0)

    DATA_PATH = sys.argv[1]
    if not os.path.exists(DATA_PATH):
        print(DATA_PATH+" doesn't exist.")
    else:
        getQuery(DATA_PATH)