"""Скрипт для сбора информации о подключенных абонентах на OLT HUAWEI MA5608T"""

import re
import csv
import os
import getpass
import sys
import telnetlib
import time
# from ipaddress import *
# hosts = IPv4Network(sys.argv[1])

# При запуске скрипта необходимо указать хост устройства,
# затем ввести логин и пароль в соответствующих строках

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

    # Отключение пагинации (скроллинга) на SNR
    # tn.write(b'terminal length 0\n')
    tn.write(b'enable\r\n')
    time.sleep(1)

    tn.write(b'scroll\r\n\r\n')
    time.sleep(1)

    tn.write(b'display board 0/0\r\n')
    time.sleep(10)
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

pattern = re.compile(r'(\d/)\s(\d/\d)\s+(\d{1,2})\s+.+(\d{8,10})(_.*)\((.*?)\)')

lines = []

for line in output:
    if re.findall(pattern, line):
        line = list(re.findall(pattern, str(line))[0])
        lines.append(line)
        # print(line)
        with open(os.path.join(host + '.csv'), 'w') as data:
            writer = csv.writer(data)
            writer.writerows(lines)
