import sys
import os
import datetime
import sqlite3
import csv


def checkTimeFormat(time,error_at):
    try:
        datetime.datetime.strptime(time,"%Y-%m-%d %H:%M")
        return True
    except ValueError:
        print("Incorrect time format at "+error_at+", should be YYYY-MM-DD HH:MM")
        return False

def checkPath(dir_path):
    if not os.path.exists(dir_path):
        print("path:["+dir_path+"] doesn't exist.")
        return False
    filenames = os.listdir(dir_path)
    if len([filename for filename in filenames if filename.endswith('.csv')]) < 1:
        print('No log file in directory')
        return False
    return True

def getQuery(DATA_PATH):
    con = sqlite3.Connection('newdb.sqlite')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS LOGS")
    cur.execute('CREATE TABLE LOGS (timestamp int, IP text, cpu_id int, usage int);')

    filenames = os.listdir(DATA_PATH)
    csv_file = os.path.join(DATA_PATH, [filename for filename in filenames if filename.endswith('.csv')][0])

    f = open(csv_file)
    csv_reader = csv.reader(f, delimiter=',')

    cur.executemany('INSERT INTO LOGS VALUES (?, ?, ?, ?)', csv_reader)
    con.commit()
    f.close()

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
        start_time = words[3]+' '+words[4]
        end_time = words[5]+ ' '+words[6]

        if not checkTimeFormat(start_time,'start_time') or not checkTimeFormat(end_time,'end_time'):
            continue

        start_time = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M")
        print(start_time,end_time)

        # cur.execute("SELECT * FROM LOGS")
        # con.commit()
        #
        # rows = cur.fetchall()
        # print(rows)

        cur.execute("SELECT * FROM LOGS where IP = '%s' and cpu_id = %s and timestamp >= %d and timestamp < %d"
                    % (ip,cpu_id,start_time.timestamp(),end_time.timestamp()))
        con.commit()

        rows = cur.fetchall()
        print(len(rows))

        for row in rows:
            print('(%s, %s%%)'%(datetime.datetime.fromtimestamp(row[0]),row[3]))


    cur.close()
    con.commit()
    con.close()


        # # check if directory exists
        # if not checkPath(os.path.join(DATA_PATH,ip)):
        #     print('Incorrect IP address')
        #     continue
        #
        # if not checkPath(os.path.join(DATA_PATH,ip,cpu_id)):
        #     print('Incorrect CPU Id address')
        #     continue
        #
        # logs = []
        # # check if csv exists
        # for i in range(len(timestamps)):
        #     if not os.path.isfile(os.path.join(DATA_PATH, ip, cpu_id, (str(timestamps[i])+'.csv'))):
        #         print('Incorrect time interval.')
        #         print("Logs for day:",datetime.datetime.fromtimestamp(timestamps[i]).date()," is not available.")
        #         continue
        #     if i == 0:
        #         print("CPU",cpu_id," usage on ",ip)
        #     with open(os.path.join(DATA_PATH, ip, cpu_id, (str(timestamps[i])+'.csv'))) as f:
        #         lines = f.readlines()
        #         if len(timestamps) == 1:
        #             # no_minutes = int((end_time-start_time).total_seconds()/60)
        #             # print(start_time.hour,start_time.hour*60,start_time.minute,(start_time.hour*60)+start_time.minute )
        #             # print(end_time.hour,end_time.hour*60,end_time.minute,(end_time.hour*60)+end_time.minute )
        #             start_index = (start_time.hour*60)+start_time.minute
        #             end_index = (end_time.hour*60)+end_time.minute
        #             for t in range(start_index,end_index):
        #                 time = '{:02d}:{:02d}'.format(*divmod(t, 60))
        #                 usage = lines[t].split(',')[-1].rstrip()
        #                 print('(%s %s %s%%)'%(datetime.datetime.fromtimestamp(timestamps[i]).date(),time,usage))


        # read csv


# QUERY 192.168.1.10 1 2021-06-23 01:05 2021-06-23 01:10

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give path to directory.')
        print('Usage: python query.py [Path to Directory]')
        exit(0)

    DATA_PATH = sys.argv[1]
    if checkPath(DATA_PATH):
        getQuery(DATA_PATH)