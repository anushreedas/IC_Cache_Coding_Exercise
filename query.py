"""
This program implements a command line tool which takes a directory of data files as a parameter
and lets you query CPU usage for a specific CPU in a given time period.
It is an interactive command line tool which read a user’s commands from stdin.
@author : Anushree Das
"""
import sys
import os
import datetime
import sqlite3
import csv


def checkPath(dir_path):
    """
    Checks if the directory exits.
    Also checks if there is a csv file in the directory.
    :param dir_path: directory containing csv file with all logs
    :return: True/False
    """
    # Checks if the directory exits
    if not os.path.exists(dir_path):
        print("path:["+dir_path+"] doesn't exist.")
        return False

    # checks if there is a csv file in the directory
    filenames = os.listdir(dir_path)
    if len([filename for filename in filenames if filename.endswith('.csv')]) < 1:
        print('No log file in directory')
        return False

    return True


def getQuery(DATA_PATH):
    """
    Reads logs from the directory and runs a command line tool to take query as input from user.
    :param DATA_PATH: path to directory containing csv file with all logs
    :return: None
    """

    # Create sql table to store logs for easy querying
    con = sqlite3.Connection('newdb.sqlite')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS LOGS")
    cur.execute('CREATE TABLE LOGS (timestamp int, IP text, cpu_id int, usage int);')

    # find csv file with logs
    filenames = os.listdir(DATA_PATH)
    csv_file = os.path.join(DATA_PATH, [filename for filename in filenames if filename.endswith('.csv')][0])

    # read logs from csv file
    f = open(csv_file)
    csv_reader = csv.reader(f, delimiter=',')

    # insert logs from csv to sql table
    cur.executemany('INSERT INTO LOGS VALUES (?, ?, ?, ?)', csv_reader)
    con.commit()

    f.close()

    # loop until user inputs 'EXIT'
    while True:
        # take commamd as input from user in stdin
        command = input('\n>')

        # if user inputs 'EXIT' then stop loop
        if str.lower(command) == 'exit':
            break

        # check query command format is correct
        # check if first word in command given by the user is 'QUERY'
        words = command.split(' ')
        if str.lower(words[0]) != 'query' or len(words) != 7:
            print('Query syntax: QUERY IP cpu_id time_start time_end')
            print('Example: QUERY 192.168.1.10 1 2014-10-31 00:00 2014-10-31 00:05')
            print("Enter 'EXIT' to stop.")
            continue

        # check if IP address entered is of correct format
        ip = words[1]
        if len([s for s in ip.split('.') if s.isdigit()]) != 4:
            print('Incorrect IPv4 address entered.')
            continue

        # check if CPU Id entered is of correct format
        cpu_id = words[2]
        if not cpu_id.isdigit():
            print('Incorrect CPU ID entered.')
            continue

        # check date time format
        start_time = words[3]+' '+words[4]
        end_time = words[5]+' '+words[6]

        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect time format at start_time, should be YYYY-MM-DD HH:MM")
            continue
        try:
            end_time = datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect time format at end_time, should be YYYY-MM-DD HH:MM")
            continue

        # query logs from database
        print('\nCPU%s usage on %s:\n'%(cpu_id,ip))

        cur.execute("SELECT * FROM LOGS WHERE IP = '%s' AND cpu_id = %s AND timestamp >= %d AND timestamp < %d "
                    "ORDER BY timestamp" % (ip,cpu_id,start_time.timestamp(),end_time.timestamp()))
        con.commit()

        # print logs
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append('(%s, %s%%)'%(datetime.datetime.fromtimestamp(row[0]),row[3]))
        print(*result,sep=',')

    cur.close()
    con.commit()
    con.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give path to directory.')
        print('Usage: python query.py [Path to Directory]')
        exit(0)

    DATA_PATH = sys.argv[1]
    if checkPath(DATA_PATH):
        getQuery(DATA_PATH)