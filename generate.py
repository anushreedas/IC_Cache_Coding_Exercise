"""
This program generates the logs for one day (today) for n (1000) servers,
where each server has 2 CPUs, and writes the data to csv file in the provided directory path.

@author : Anushree Das
"""
import sys
import math
from datetime import datetime, timedelta
import os
from random import randrange
import ipaddress

TODAY = datetime.now().now().replace(hour=0, minute=0, second=0, microsecond=0)


def generateLogs(DATA_PATH,date=TODAY,no_of_servers=1000, no_of_cpus=2):
    """
    Generates logs for the given number of servers for the given date
    :param DATA_PATH:       path to directory where to save data
    :param date:            date for which to generate logs
    :param no_of_servers:   number of servers
    :param no_of_cpus:      number of CPUs
    :return:                None
    """
    print('Generating logs for %d servers at DATA_PATH=[%s] for date: %s'%(no_of_servers,DATA_PATH,date.date()))

    # calculate mask for network from given number of servers
    mask = 32-math.ceil(math.log(no_of_servers, 2))

    # get ip addresses for servers
    ip_addresses = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/'+str(mask))][:no_of_servers]

    for host_ip in ip_addresses:
        for cpu_id in range(1,no_of_cpus+1):

            # Checks if the directory path exists and if it doesn't then it creates it
            if not os.path.exists(DATA_PATH):
                os.makedirs(DATA_PATH)

            date_file = os.path.join(DATA_PATH, 'logs.csv')
            with open(date_file,'a') as f:
                # write log for every minute in a day (24 * 60 minutes)
                for t in range(1440):
                    timestamp = int(datetime.timestamp(date+timedelta(minutes=t)))
                    # CPU usage is a random number between 0% to 100%
                    cpu_usage = randrange(0, 100)
                    f.write(str(timestamp)+','+host_ip+','+str(cpu_id)+','+str(cpu_usage)+'\n')

    print('Done.')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give path to directory.')
        print('Usage: python generate.py [Path to Directory]')
        exit(0)

    DATA_PATH = sys.argv[1]
    generateLogs(DATA_PATH)