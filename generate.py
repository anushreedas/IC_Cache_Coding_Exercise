import math
from datetime import datetime
import os
from random import randrange
import ipaddress


def generateLogs(directory,date):
    timestamp = int(datetime.timestamp(date))
    # print(timestamp)
    dirPath = os.path.join(directory,str(timestamp))

    if not os.path.exists(dirPath):
        print("Creating directory..")
        os.makedirs(dirPath)

    n = 1000
    mask = 32-math.ceil(math.log(n, 2))
    # print(mask)

    ipAddresses = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/'+str(mask))][:n]

    # for _ in range(1440):
    for host_ip in ipAddresses:
        for cpu_id in range(1,3):
            cpu_usage = randrange(0,100)
            print(host_ip,cpu_id,cpu_usage)

if __name__ == "__main__":
    today = datetime.now().now().replace(hour=0, minute=0, second=0, microsecond=0)
    directory = 'data'
    generateLogs(directory, today)