from threading import Thread
from jinja2 import Template
from netmiko import ConnectHandler
from glob import glob
import yaml

devices_info = [
{"hostname": "xrv1", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.101"},
{"hostname": "xrv2", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.102"},
{"hostname": "xrv3", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.103"},
{"hostname": "xrv4", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.104"},
{"hostname": "xrv5", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.105"},
{"hostname": "xrv6", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.106"},
{"hostname": "xrv7", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.107"},
{"hostname": "xrv8", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.108"},
{"hostname": "xrv9", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.109"},
{"hostname": "xrv10", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.110"},
{"hostname": "xrv11", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.111"},
{"hostname": "xrv12", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.112"},
{"hostname": "xrv13", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.113"},
{"hostname": "xrv14", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.114"},
{"hostname": "xrv15", "port": 22, "username": "admin", "password":"admin","device_type":"cisco_xr","ip":"172.20.3.115"},
]


def get_config(hostname, temp_type):
    temp_path="../config_template/"
    if "xrv" in hostname:
        device_type = "xrv"
    elif "IOS" in hostname:
        device_type = "vios"

    template_file = glob(temp_path + device_type + "_" + temp_type + "*")
    template = Template(open(template_file[0]).read())

    data_path = "../data/"
    data_file = glob(data_path + temp_type + "/" + hostname + "_*" )
    data = yaml.load(open(data_file[0]).read())
    if hostname.startswith("xrv"):
        return template.render(**data,commit=True)
    elif hostname.startswith("vIOS"):
        return template.render(**data)

def set_config(device):

    cfgs = get_config(device.get("hostname"), "bgp")
    print(cfgs)
    del device["hostname"]
    net_connect = ConnectHandler(**device)
    net_connect.send_config_set(cfgs)
    

if __name__ == '__main__':
    tasks = []
    for device in devices_info:
        task = Thread(target=set_config, args=(device,))
        task.start()
        tasks.append(task)
    for task in tasks:
        task.join()
        
