#coding: utf-8
import re
import time
import telnetlib

class Telnet(object):
    
    def __init__(self, host, port, username="admin", password="admin", device_type="iosxr", timeout=2, debug=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.debug = debug
        self.timeout = timeout
        
        '''
        deivce_type should be ["iosxr", "ios"]
        '''
        self.device_type = device_type
        
        self.login()
        
    def sendcmd(self, cmd, sleep_time=0.5):
        if isinstance(cmd, str):
            cmd = str.encode(cmd)
        self.tn.write(cmd + b"\n")
        time.sleep(sleep_time)

    def login(self):
        self.tn = telnetlib.Telnet(host=self.host, port=self.port)
        
        if self.debug:
            self.tn.set_debuglevel(7)
        
        '''send return key 
           console 在idle 时，需要先发送一个return key 才能到登录界面。
           如:
           ios con0/0/CPU0 is now available
 
 
           Press RETURN to get started.
        '''
        self.sendcmd("\r")
        
        for _ in range(0, 2):
            '''
            创建一个登录过程中，希望读到的字符串。在python3 的telnetlib中，需要bytes类型。
            如果看到 Username： 那么就发送 用户名。
            如果看到 Password： 就发送 密码。
            如果看到 RP/0/0/CPU0 就说明已经登录了。 在这个LAB中，所有的设备只有单引擎。因此在IOS XR 上都是 RP/0/0/CPU0
            如果看到是 Router 就说明已经登录完成了。在这个LAB中，vIOS设备在没有配置的时，hostname 默认是 Router
            '''
            expect_list = []
            expect_list.append(re.compile(b"username:", re.I))       # re.I 不区分大小写
            expect_list.append(re.compile(b"password:",re.I))        # re.I 不区分大小写
            expect_list.append(re.compile(b"RP/0/0/CPU0", re.I))     # re.I 不区分大小写
            expect_list.append(re.compile(b"Router"))
            expect_list.append(re.compile(b"ios", re.I))
        
            result = self.tn.expect(expect_list, timeout=self.timeout)
            if result[0] == 0:
                 self.sendcmd(self.username)
            elif result[0] == 1:
                self.sendcmd(self.password)
            elif result[0] in [2, 3, 4]:
                print("Login right")
                self.set_terminal_lenght_zero()
                break
            else:
                print("Login Fail")
                
    def set_terminal_lenght_zero(self):
        if self.device_type.lower() == "ios":
            self.sendcmd("enable")
        self.sendcmd("terminal length 0")

    def config_hostname(self, hostname):
        if self.device_type.lower() == "ios":
            self.sendcmd("enable")
        self.sendcmd("config terminal")
        self.sendcmd("hostname %s" %hostname)
        
        if self.device_type.lower() == "iosxr":
            self.sendcmd("commit")
        
        self.sendcmd("end")
        
    def send_config_set(self, cfgs):
        self.sendcmd("config terminal")
        for line in cfgs:
            self.sendcmd(line)
        
        if self.device_type.lower() == "iosxr":
            self.sendcmd("commit")
        
        self.sendcmd("end")
        
        
    
    def __del__(self):
        self.tn.close()
        
    
if "__main__" == __name__:
    tn = Telnet(host="172.20.0.1", port=33281, device_type="iosxr", debug=True)
    tn.config_hostname("xrv1")
    
    
