import math
from datetime import datetime
import os
from random import randrange
import ipaddress

def createDirectory(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

def generateLogs(directory,date):
    timestamp = int(datetime.timestamp(date))
    # print(timestamp)

    n = 2
    mask = 32-math.ceil(math.log(n, 2))
    # print(mask)

    ipAddresses = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/'+str(mask))][:n]

    for host_ip in ipAddresses:
        server_path = os.path.join(directory,host_ip)
        createDirectory(server_path)
        for cpu_id in range(1,3):
            cpu_path = os.path.join(server_path,str(cpu_id))
            createDirectory(cpu_path)
            date_file = os.path.join(cpu_path, str(timestamp)+'.csv')
            # createDirectory(date_file)
            with open(date_file,'w') as f:
                for _ in range(1440):
                    cpu_usage = randrange(0, 100)
                    print(host_ip, cpu_id, cpu_usage)
                    f.write(str(timestamp)+','+host_ip+','+str(cpu_id)+','+str(cpu_usage)+'\n')

if __name__ == "__main__":
    today = datetime.now().now().replace(hour=0, minute=0, second=0, microsecond=0)
    directory = 'data'
    generateLogs(directory, today)