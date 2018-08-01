# 登录实验环境
## 1.0 实验环境软件介绍
实验环境使用的是[eve-ng](http://www.eve-ng.net/)软件。安装在物理服务器上。

 ---------------
EVE-NG（全称Emulated Virtual Environment - Next Generation），继Unetlab 1.0后的Unetlab的2.0新版本，改了名字，原名是Unified Networking Lab统一网络实验室。笔者觉得名字改的非常合理，这款模拟器已经不仅可以模拟网络设备，也可以运行一切虚拟机。理论上，只要能将虚拟机的虚拟磁盘格式转换为qcow2都可以在EVE-NG上运行。所以，EVE-NG可以算得上是仿真虚拟环境。
 -----------

## 2.0 实验环境信息
### 2.1 服务器登录信息
#### 2.1.1 Linux登录信息:

IP | port| protocol| username| password
---|----|----|---|---|-----
10.74.82.244|22|SSH|lab|Cisco,123
10.74.82.253|22|SSH|lab|Cisco,123

ssh private key:

[private key] (../ssh_key/eve_sha_rsa)

[public key] (../ssh_key/eve_sha_rsa.pub)

MAC OS ssh config:

```
path: $HOME/.ssh/config
Host eve1
     Hostname 10.74.82.244
     user lab
     IdentityFile ~/.ssh/eve_sha_rsa

Host eve2
     Hostname 10.74.82.253
     user lab
     IdentityFile ~/.ssh/eve_sha_rsa     
```

#### 2.1.2 web登录信息:
IP | port| protocol| username| password
---|----|----|---|---|-----
10.74.82.244|80|http|netdevops|netdevops
10.74.82.253|80|http|netdevops|netdevops

#### 2.1.3 登录到模拟的网络设备
Console 登录：

```
telnet 10.74.82.224 <port>
```
Port 信息的获取：

 - 1. 通过 web登录后获取。
 - 2. 见设备信息文件。
 
SSH 登录设备：

#### 1. 先登录到eve的宿主机，然后在登录到每台设备。
 
```
 ssh eve[1-2] 
 ssh -l <username> <Device IP>
```
   - \<username> 见设备设备信息文件。默认为admin
   - \<Device IP> 见设备IP地址分配文件。
  
#### 2. 通过SSH命令直接登录到网络设备。
 
 ```
 ssh -J eve[1-2] -l <username> <Device IP>
 ```
   - -J eve[1-2] 为SSH跳板



 
 
 




