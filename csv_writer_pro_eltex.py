"""Скрипт для сбора информации о подключенных абонентах на OLT ELTEX LTP-8X"""

import re
import csv
import os
import getpass
import sys
import telnetlib
import time
# from ipaddress import *
# hosts = IPv4Network(sys.argv[1])

username = input('Enter your remote account: ')
password = getpass.getpass()
port = 23
host = sys.argv[1]
connection_timeout = 5
reading_timeout = 5
# for host in IPv4Network(hosts):

try:
    tn = telnetlib.Telnet(host, port, connection_timeout)
    tn.read_until(b'name:', reading_timeout)
    tn.write((username + '\r\n').encode())

    tn.read_until(b'password:', reading_timeout)
    tn.write((password + '\r\n').encode())

    tn.write(b'show interface ont 0-7 configured\r\n')
    time.sleep(5)

except Exception as err:
    print('Произошла ошибка %s' % err)

try:
    output = (tn.read_very_eager()).decode().split('\n')
    # print(output, type(output))
    # for line in output:
    #     print(line)
except Exception as err:
    print(err)
tn.close()

pattern = re.compile(r'(\d{8,10})(_.*)\((.*?)\)')

lines = []

for line in output:
    if list(re.findall(r'(\d{8,10})(_.*)\((.*?)\)', str(line))):
        line = ['0/','0/'+line.split()[3], line.split()[2]] + list(re.findall(pattern, str(line))[0])
        lines.append(line)
        with open(os.path.join(host + '.csv'), 'w') as data:
            writer = csv.writer(data)
            writer.writerows(lines)
