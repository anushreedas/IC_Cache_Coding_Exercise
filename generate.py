"""
This program generates the logs for one day (today) for n (1000) servers,
where each server has 2 CPUs, and writes the data to csv files in the provided directory path.

@author : Anushree Das
"""
import math
from datetime import datetime
import os
from random import randrange
import ipaddress


def createDirectory(dir_path):
    """
    Checks if the directory path exists
    and if it doesn't then it creates it
    :param dir_path: directory path
    :return: None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def generateLogs(DIRECTORY,date,no_of_servers, no_of_cpus):
    """
    Generates logs for the given number of servers for the given date
    :param DIRECTORY:       path to directory where to save data
    :param date:            date for which to generate logs
    :param no_of_servers:   number of servers
    :param no_of_cpus:      number of CPUs
    :return:                None
    """
    print('Generating logs for %d servers for date: %s'%(no_of_servers,date.date()))

    # get timestamp in Unix time for given date
    timestamp = int(datetime.timestamp(date))

    # calculate mask for network from given number of servers
    mask = 32-math.ceil(math.log(no_of_servers, 2))

    # get ip addresses for servers
    ip_addresses = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/'+str(mask))][:no_of_servers]

    for host_ip in ip_addresses:
        server_path = os.path.join(DIRECTORY,host_ip)
        createDirectory(server_path)

        for cpu_id in range(1,no_of_cpus+1):
            cpu_path = os.path.join(server_path,str(cpu_id))
            createDirectory(cpu_path)

            # write log to csv file at path [DIRECTORY/server_ipaddr/cpu_id/timestamp.csv]
            date_file = os.path.join(cpu_path, str(timestamp)+'.csv')
            with open(date_file,'w') as f:
                # write log for every minute in a day (24 * 60 minutes)
                for _ in range(1440):
                    # CPU usage is a random number between 0% to 100%
                    cpu_usage = randrange(0, 100)
                    f.write(str(timestamp)+','+host_ip+','+str(cpu_id)+','+str(cpu_usage)+'\n')

    print('Done.')


def generateLogsSimulator(DIRECTORY):
    today = datetime.now().now().replace(hour=0, minute=0, second=0, microsecond=0)
    no_of_servers = 1000
    no_of_cpus = 2

    generateLogs(DIRECTORY, today, no_of_servers,no_of_cpus)


if __name__ == "__main__":
    DIRECTORY = 'data'
    generateLogsSimulator(DIRECTORY)