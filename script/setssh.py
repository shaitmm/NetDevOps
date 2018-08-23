from jinja2 import Template
from telnet import Telnet
import threading

devices_info = [{'port': 33296, 'hostname': 'vIOS16', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.116"},
                {'port': 33297, 'hostname': 'vIOS17', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.117"},
                {'port': 33298, 'hostname': 'vIOS18', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.118"},
                {'port': 33299, 'hostname': 'vIOS19', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.119"},
                {'port': 33300, 'hostname': 'vIOS20', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.120"},
                {'port': 33301, 'hostname': 'vIOS21', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.121"},
               ]


def render_temp(device):
    ssh_template = "../config_template/vios_ssh.j2"
    ssh_template = Template(open(ssh_template).read())
    cfgs = ssh_template.render(hostname=device.get("hostname"))
    cfgs = cfgs.splitlines()
    return cfgs

def set_ssh(device):
    cfgs = render_temp(device)
    
    tn = Telnet(host="172.20.0.1", port=device.get("port"), device_type="ios", debug=True) 
    tn.send_config_set(cfgs)


if __name__ == "__main__":
    thread_tasks = []
    for device in devices_info:
        task = threading.Thread(target=set_ssh, args=(device,))
        task.start()
        thread_tasks.append(task)
    for t in thread_tasks:
        t.join()
