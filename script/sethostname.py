#import sys
#sys.path.append("../lib")

from telnet import Telnet
'''
devices_info = [{'port': 33281, 'hostname': 'xrv1', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.101"},
                {'port': 33282, 'hostname': 'xrv2', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.102"},
                {'port': 33283, 'hostname': 'xrv3', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.103"},
                {'port': 33284, 'hostname': 'xrv4', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.104"},
                {'port': 33285, 'hostname': 'xrv5', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.105"},
                {'port': 33286, 'hostname': 'xrv6', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.106"},
                {'port': 33287, 'hostname': 'xrv7', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.107"},
                {'port': 33288, 'hostname': 'xrv8', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.108"},
                {'port': 33289, 'hostname': 'xrv9', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.109"},
                {'port': 33290, 'hostname': 'xrv10', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.110"},
                {'port': 33291, 'hostname': 'xrv11', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.111"},
                {'port': 33292, 'hostname': 'xrv12', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.112"},
                {'port': 33293, 'hostname': 'xrv13', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.113"},
                {'port': 33294, 'hostname': 'xrv14', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.114"},
                {'port': 33295, 'hostname': 'xrv15', 'username': 'admin', 'password': 'admin',"mgt_ip": "172.20.3.115"},
                {'port': 33296, 'hostname': 'vIOS16', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.116"},

               ]
'''

devices_info = [{'port': 33296, 'hostname': 'vIOS16', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.116"},
                {'port': 33297, 'hostname': 'vIOS17', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.117"},
                {'port': 33298, 'hostname': 'vIOS18', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.118"},
                {'port': 33299, 'hostname': 'vIOS19', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.119"},
                {'port': 33300, 'hostname': 'vIOS20', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.120"},
                {'port': 33301, 'hostname': 'vIOS21', 'username': 'admin', 'password': 'admin', "mgt_ip": "172.20.3.121"},
               ]

for d in devices_info:
    device_type =""
    if "xrv" in d.get("hostname"):
        device_type = "iosxr"
    if "IOS" in d.get("hostname"):
        device_type = "ios" 
    tn = Telnet(host="172.20.0.1", port=d.get("port"), device_type=device_type, debug=True)
    tn.config_hostname(d.get("hostname"))

