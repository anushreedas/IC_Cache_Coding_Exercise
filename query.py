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
        command = input('\n>')
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
        end_time = words[5]+' '+words[6]

        if not checkTimeFormat(start_time,'start_time') or not checkTimeFormat(end_time,'end_time'):
            continue

        start_time = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M")

        print('\nCPU%s usage on %s:\n'%(cpu_id,ip))

        cur.execute("SELECT * FROM LOGS WHERE IP = '%s' AND cpu_id = %s AND timestamp >= %d AND timestamp < %d "
                    "ORDER BY timestamp" % (ip,cpu_id,start_time.timestamp(),end_time.timestamp()))
        con.commit()

        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append('(%s, %s%%)'%(datetime.datetime.fromtimestamp(row[0]),row[3]))
        print(*result,sep=',')

    cur.close()
    con.commit()
    con.close()


# QUERY 192.168.1.10 1 2021-06-23 01:05 2021-06-23 01:10

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give path to directory.')
        print('Usage: python query.py [Path to Directory]')
        exit(0)

    DATA_PATH = sys.argv[1]
    if checkPath(DATA_PATH):
        getQuery(DATA_PATH)