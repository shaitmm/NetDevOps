import pexpect
from pexpect import EOF, TIMEOUT
import sys

class DeviceBase(object):

    def __init__(self, params):

        self.params = params
        self.hostname = params.get("hostname")
        self.port = params.get("port", 22)
        self.username = params.get("username", "lab")
        self.password = params.get("password", "lab")
        self.connect_type = params.get("connect_type", "ssh")
        self.device_type = params.get("device_type", "iosxr")

        self.debug = params.get("debug", 0)
        self.verbose = params.get("verbose", False)


        self.expect_list = []


    def _telnet(self):

        cmd = "telnet {hostname} {port}".format(hostname=self.hostname, port=self.port)
        return cmd


    def _ssh(self):
        ssh = "ssh {hostname} -l {username} " \
              " -p {port} " \
              "-o StrictHostKeyChecking=no " \
              "-o UserKnownHostsFile=/dev/null".format(username=self.username,
                                                       hostname=self.hostname,
                                                       port=self.port)
        return ssh

    def connect(self, timeout=5):
        if self.connect_type.lower() == "ssh":
            self.c =pexpect.spawn(self._ssh(), encoding="utf-8")

        elif self.connect_type.lower() == "telnet":
            self.c = pexpect.spawn(self._telnet(), encoding="utf-8")
        else:
            raise ("connect error")

        self.c.delaybeforesend = 1
        self.c.timeout = timeout
        self.c.logfile = sys.stdout

        return self.c

    def get_prompt(self):
        self.c.sendline()
        self.c.expect(r"[>|#|$]\s?$")
        prompt = self.c.before.strip("\r\n")
        prompt += self.c.after
        self.prompt = prompt



    def login(self, prompt=r"[>|#|$]\s?$"):
        self.expect_list = []
        self.expect_list.append(r"(?i)username[:]?\s*$")    # username
        self.expect_list.append(r"(?i)login[:]?\s*$")       # login
        self.expect_list.append(r"(?i)password[:]?\s*$")    # password
        # self.expect_list.append(r"secret:\s*$")           # IOS-XR init config
        self.expect_list.append(prompt)
        self.c.send("\n\r")
        for _ in range(0, 3):
            result = []

            try:
                i = self.c.expect(self.expect_list, timeout=5)
                result.append(i)
                result.append(str(self.c.before))
                result.append(str(self.c.after))
                if i == 0 or i == 1:
                    self.c.sendline(self.username)
                elif i == 2:
                    self.c.sendline(self.password)
                elif i == 3:
                    break
            except EOF:
                break
            except TIMEOUT:
                print("connect to %s timeout" % self.hostname)
                break

        if result[0] < 3:
            print(result)
            print("username or password error")
            return result

        self.get_prompt()

        self._set_terminal_length_zero()
        return result

    def _set_terminal_length_zero(self):
        pass

    def logout(self):
        if self.c:
            self.c.terminate()

    def __del__(self):
        self.logout()


class IOSXR(DeviceBase):

    def to_config_mode(self, prompt="\)\#"):
        self.c.sendline("config terminal")
        try:
            i = self.c.expect(prompt, timeout=2)
            if i == 0:
                print("in the config mode")
        except TIMEOUT:
            print("session timeout")


    def send_config(self, cmd, prompt="\)\#"):
        self.c.sendline(cmd)
        try:
            i = self.c.expect(prompt, timeout=2)
            if i == 0:
                print("send command %s" %cmd)

        except Exception as e:
            print(e)
    
    def to_enable(self, prompt="\#$"):
        self.c.sendline("end")
        if self.c.expect(prompt, timeout=2):
            print("to enable")
    
    def send_command(self, cmd, prompt="\#$"):
        self.c.sendline(cmd)
        result = []
        i = self.c.expect(prompt, timeout=2)
        if i == 0:
            print("sent command %s" %cmd)
            result.append(i)
            result.append(str(self.c.before))
            return result

    def _set_terminal_length(self):
        self.c.sendline("terminal length 0")
        try:
            i = self.c.expect(self.prompt)
        except EOF:
            pass
        except TIMEOUT:
            print("session timeout")

    def get_config(self):
        self.expect_list = []
        self.expect_list.append(self.prompt)
        print(self.prompt)
        result = []
        self.c.sendline("show running-config")
        try:
            i = self.c.expect(self.expect_list, timeout=5)
            if i == 0:
                result.append(i)
                result.append(str(self.c.before))
                result.append(str(self.c.after))
        except EOF:
            pass
        except TIMEOUT:
            print("session timeout")
        return result


if __name__ == "__main__":

    device = {"hostname": "172.20.0.1",
              "port":33281,
              "username": "yuxin",
              "password": "yuxin123",
              "connect_type": "telnet",
              "device_type": "iosxr"}
    d = IOSXR(device)
    d.connect()
    d.login()
    #d.get_prompt()
    print(d.get_config())
