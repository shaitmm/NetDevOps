# 定制一个eve下的img

## 1 定制一个vIOS img
vIOS的默认img

vIOS 需要的是一个32bits的模拟环境。因此需要使用qemu来模拟一个32bits的CPU。

### 1.1 启动一个vIOS的img:
```
qemu-system-i386 -nographic -m 512 -hda virtioa.qcow2  -serial telnet::5000,server,nowait -net nic,model=e1000

QEMU 2.5.0 monitor - type 'help' for more information
(qemu) Warning: vlan 0 is not connected to host network

```
-nographic: 启动的时候不需要显卡

-m 512: 启动的时分配512M的内存

-hda virtioa.qcow2: 启动使用的磁盘文件是virtioa.qcow2

-serial telnet::5000,server,nowait: 定义个console口。server指将做为一个telnet server的行为。

-net nic,model=e1000: 定义个网卡

### 1.2 登录这台vIOS设备

```
telnet localhost 5000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Booted IOSv. Boot args: [/vios-adventerprisek9-m]

Smart Init is enabled
<省略部分信息...>
Processor board ID 9GDTC9XN1M6W2C3NGCI9K
1 Gigabit Ethernet interface
DRAM configuration is 72 bits wide with parity disabled.
256K bytes of non-volatile configuration memory.
2097144K bytes of ATA System CompactFlash 0 (Read/Write)
0K bytes of ATA CompactFlash 1 (Read/Write)
0K bytes of ATA CompactFlash 2 (Read/Write)
0K bytes of ATA CompactFlash 3 (Read/Write)


         --- System Configuration Dialog ---

Would you like to enter the initial configuration dialog? [yes/no]:
% Please answer 'yes' or 'no'.
Would you like to enter the initial configuration dialog? [yes/no]:
% Please answer 'yes' or 'no'.
```
### 1.3 配置这台vIOS设备

```
Would you like to enter the initial configuration dialog? [yes/no]: no


Press RETURN to get started!


*Mar  1 00:00:02.052: %ATA-6-DEV_FOUND: device 0x1F0
*Mar  1 00:00:13.016: %NVRAM-5-CONFIG_NVRAM_NOT_FOUND: NVRAM configuration 'flash:/nvram' could not be found on disk.
*Jul 31 01:10:02.271: %PA-3-PA_INIT_FAILED: Performance Agent failed to initialize (Missing Data License)
*Jul 31 01:10:08.441: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up
*Jul 31 01:10:09.555: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to up
<省略部分信息...>

Router>
Router>
Router>
Router>en
Router#copy running-config startup-config
Destination filename [startup-config]?
Building configuration...
[OK]
```

### 1.4 查看设备的接口信息
由于在启动的时候只定义了一个网卡。因此，这台设备只有一个网络接口。
```
Router#show interfaces stats
Interface GigabitEthernet0/0 is disabled
```

### 1.5 关闭这台vIOS
在qemu的控制台上。stop这台vIOS。并ctrl+c退出。
```
(qemu)
(qemu) stop
(qemu) qemu-system-i386: terminating on signal 2 
root@eve-1:~/vios#
```

### 1.6 把定制好的vIOS复制到 eve的目录中

```
cp virtioa.qcow2 /opt/unetlab/addons/qemu/vios-adventerprisek9-m-15.6.2T/virtioa.qcow2
```

## 2 为xrvr添加一个pie（SMU）
xrvr需要一个64bits的运行环境，因此需要用qemu-system-x86_64来模拟一个64bits的环境。

我们需要给一个xrvr镜像添加一个pie。

### 2.1 创建一个包含pie的磁盘文件

#### 2.1.1 创建一个磁盘文件

```
qemu-img create -f raw pie.qcow2 1G
```
create: 创建一个磁盘文件

-f raw: 定义磁盘文件的格式

pie.qcow2: 为磁盘文件的文件名

1G:  磁盘文件分配的空间

#### 2.1.2 在磁盘文件中添加文件内容

在运行guestfish的时，需要有root的权限。或者直接先用sudo -s 切换到root用户。
```
    # guestfish -a pie.qcow2
    
    Welcome to guestfish, the guest filesystem shell for
    editing virtual machine filesystems and disk images.
    
    Type: 'help' for help on commands
          'man' to read the manual
          'quit' to quit the shell
    
    ><fs> run
    ><fs> list-filesystems
    /dev/sda: vfat
    ><fs> mount /dev/sda /
    ><fs> ls /
    ><fs> upload xrvr-k9sec-x.pie-6.5.1.31I /xrvr-k9sec-x.pie-6.5.1.31I
    ><fs> ls /
    xrvr-k9sec-x.pie-6.5.1.31I
    ><fs>
    
```
### 2.2 启动xrvr的镜像
```
qemu-system-x86_64 -nographic -m 3072 -hda iosxrv-6.5.1.31I.qcow2  -hdb pie.qcow2 -serial telnet::12101,server,wait -serial telnet::12102,server,nowait -serial telnet::12103,server,nowait -net nic,model=virtio,vlan=1,macaddr=00:01:00:ff:00:00
```

xrvr需要更多的内存才能启动。

### 2.3 添加SMU

启动完xrvr后，和正常的设备一样来添加SMU文件。后续的动作和vIOS的一样的。最后，把这个镜像文件复制到eve的相应目录中就可以了。
```
dir disk1:/
xrvr-k9sec-x.pie-6.5.1.31I

(admin) install add disk1:/xrvr-k9sec-x.pie-6.5.1.31I
(admin) install active
(admin) install commit

```































