#!/usr/bin/python
# coding:utf-8

"""
采集机器自身信息
1 主机名
2 内存
3 ip与mac地址
4 cpu信息
5 硬盘分区信息
6 制造商信息
7 出厂日期
8 系统版本
"""
import socket
import psutil
import subprocess
import time
import platform
import json
import requests

device_white = ['ens33','eth1', 'eth2', 'eth3', 'bond0', 'bond1']


def get_hostname():
    return socket.gethostname()


def get_meminfo():
    with open("/proc/meminfo") as f:
        tmp = int(f.readline().split()[1])
        return round((tmp / 1024 / 1024 ),2)


def get_device_info():
    ret = []
    for device, device_info in psutil.net_if_addrs().items():
        if device in device_white:
            tmp_device = {}
            for sinc in device_info:
                if sinc.family == 2:
                    tmp_device['ip'] = sinc.address
                if sinc.family == 17:
                    tmp_device['mac'] = sinc.address
            ret.append(tmp_device)
    return ret

def get_cpu_info():
    ret = {'cpu':'','num':0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            tmp = line.split(":")
            key = tmp[0].strip()
            if key == "processor":
                ret['num'] += 1
            if key == "model name":
                ret['cpu'] = tmp[1].strip()
    return ret

def get_disk_info():
    cmd = """lsblk -l |grep disk """
    disk_data = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    patition_size = []
    for dev in disk_data.stdout.readlines():
        # size = int(dev.strip().split()[4]) / 1024 / 1024/ 1024
        data = str(dev)
        disk_name = data.split()[0].split("\'")[1]
        size = data.split()[3]
        patition_size.append(size)
    return " + ".join(patition_size)

# 获取制造商信息
def get_manufacturer_info():
    ret = {}
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    manufacturer_data = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in manufacturer_data.stdout.readlines():
        line = str(line)
        if 'Manufacturer' in line:
            ret['manufacturers'] = line.split(':')[1].strip().split('\\')[0]
        elif 'Product Name' in line:
            ret['server_type'] = line.split(':')[1].strip().split('\\')[0]
        elif 'Serial Number' in line:
            ret['st'] = line.split(':')[1].strip().split('\\')[0]
        elif 'UUID' in line:
            ret['uuid'] = line.split(':')[1].strip().split('\\')[0]
    return ret

# 获取出厂日期
def get_real_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    date_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    real_date = str(date_data.stdout.readline()).split(':')[1].strip().split("\\")[0]
    return time.strftime('%Y-%m-%d', time.strptime(real_date, "%m/%d/%Y"))

def get_os_version():
    return ' '.join(platform.linux_distribution())

def get_innerip(ipinfo):
    inner_device = ['ens33','eth1', 'bond0']
    ret = {}
    for info in ipinfo:
        if ( 'ip' in info)  and info.get('device', None) in inner_device:
            ret['ip'] = info.get('ip')
            ret['mac_address'] = info.get('mac')
            return ret
    return {}

def run():
    data = {}
    data['hostname'] = get_hostname()
    device_info = get_device_info()
    data.update(get_innerip(device_info))
    data['ipinfo'] = json.dumps(device_info)

    cpu_info = get_cpu_info()
    data['server_cpu'] = "{cpu} {num}".format(**cpu_info)
    data['server_disk'] = json.dumps(get_disk_info())
    data['server_mem'] = get_meminfo()
    data.update(get_manufacturer_info())
    data['manufacture_date'] = get_real_date()
    data['os'] = get_os_version()
    if 'virtualbox' == data['server_type']:
        data['vm_status'] = 0
    else:
        data['vm_status'] = 1
    # return data
    send(data)

def send(data):
    url = "http://192.168.163.136:8002/cmdb/reporting/"
    r = requests.post(url, data = data)
    print (r)
    print (data)

if __name__ == "__main__":
    run()
