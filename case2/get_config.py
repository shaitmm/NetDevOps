import pexpect
from pexpect import EOF, TIMEOUT

def ssh_connect(username, address, port):
    ssh_command = 'ssh  -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l %s %s -p %d' % (
        username, address, port)
    return pexpect.spawn(ssh_command)


class Device(object):

    def __init__(self, device):
    
        self.hostname = device.get("hostname")
        self.mgt_ip = device.get("mgt_ip")
        self.username = device.get("username")
        self.password = device.get("password")
        self.port = device.get("port", 22)
        self.expect_list = []

    def connect(self, timeout=30):
        self.c = ssh_connect(self.username, self.mgt_ip, self.port)
        self.c.delaybeforesend = 0.10
        return self.c
    # 修改 async 函数
    async def login(self, prompt=r"[>|#|$]\s?$"):
        self.expect_list = []
        self.expect_list.append(r"(?i)username[:]?\s*$")
        self.expect_list.append(r"(?i)login[:]?\s*$")
        self.expect_list.append(r"(?i)password[:]?\s*$")
        self.expect_list.append(prompt)
        for _ in range(0, 2):
            result = []
            try:
                # i = self.c.expect(self.expect_list, timeout=5)
                # 需要等待一些时间才从设备上获取值。
                i = await self.c.expect(self.expect_list, timeout=5, async_=True)
                result.append(i)
                result.append(str(self.c.before))
                result.append(str(self.c.after))
                if i < 2:
                    self.c.sendline(self.username)
                elif i == 2:
                    self.c.sendline(self.password)
                elif i == 3:
                    break
            except EOF:
                break
            except TIMEOUT:
                print("connect to %s timeout" %self.hostname)
                break
        if result and result[0] < 3:
            print("username or password error")
            return result
        
        await self._set_terminal_length_zero()
        return result

    def _set_terminal_length_zero(self):
        pass

    def get_config(self):
        pass
    
    def logout(self):
        if self.c:
            self.c.terminate()

    def __del__(self):
        self.logout()

        
class IOSXR(Device):
    def __init__(self, device):
        super(IOSXR, self).__init__(device)
        self.prompt = self.hostname + "[>|#]\s?"

   # 需要等待一些时间才从设备上获取值。
    async def login(self, prompt=""):
        if not prompt:
            prompt = self.prompt
        await super(IOSXR, self).login(prompt)

    # 需要等待一些时间才从设备上获取值。
    async def _set_terminal_length_zero(self):
        self.c.sendline("terminal length 0")
        try:
            i = await self.c.expect(self.prompt, async_=True)
        except EOF:
            pass
        except TIMEOUT:
            print("session timeout")

    # 需要等待一些时间才从设备上获取值。
    async def get_config(self):
        self.expect_list = []
        self.expect_list.append(self.prompt)
        result = []
        self.c.sendline("show running-config")
        try:
            i = await self.c.expect(self.expect_list, timeout=5, async_=True)
            if i == 0:
                result.append(i)
                result.append(str(self.c.before))
                result.append(str(self.c.after))
        except EOF:
            pass
        except TIMEOUT:
            print("session timeout")
        return result

    
if __name__ == '__main__':
    import asyncio

    xrv1 = {"hostname":"xrv1", 
            "mgt_ip":"172.20.3.101",
            "username":"admin",
            "password":"admin",
            "port": 22}

    xrv2 = {"hostname":"xrv2", 
           "mgt_ip":"172.20.3.102",
           "username":"admin",
           "password":"admin",
           "port": 22}

    xrv3 = {"hostname":"xrv3", 
            "mgt_ip":"172.20.3.103",
            "username":"admin",
            "password":"admin",
            "port": 22}

    async def get_config(device):
        con = IOSXR(device)
        con.connect()
        print("login:", con.hostname)
        await con.login()
        result = await con.get_config()
        print(result)
        return result

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(get_config(xrv1), 
                                           get_config(xrv2),
                                           get_config(xrv3)
                                          )
                           )
