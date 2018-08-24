# 登录实验环境
## 1.0 实验环境软件介绍
实验环境使用的是[eve-ng](http://www.eve-ng.net/)软件。安装在物理服务器上。

 ---------------
EVE-NG（全称Emulated Virtual Environment - Next Generation），继Unetlab 1.0后的Unetlab的2.0新版本，改了名字，原名是Unified Networking Lab统一网络实验室。笔者觉得名字改的非常合理，这款模拟器已经不仅可以模拟网络设备，也可以运行一切虚拟机。理论上，只要能将虚拟机的虚拟磁盘格式转换为qcow2都可以在EVE-NG上运行。所以，EVE-NG可以算得上是仿真虚拟环境。
 -----------

## 2.0 实验环境信息
### 2.1 客户端要求
# <font color=red>MAC OSX：</font>
#### <font color=red>可以什么也不用安装,用系统默认的工具，有terminal 就可以。</font>
#### <font color=red>最好有iterm2和git</font>
[iterm2] (https://www.iterm2.com/) https://www.iterm2.com/

# <font color=red>Windows 10：</font>
## <font color=red>**必须**安装Putty or SecureCRT</font>
[Putty] (https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html


### 2.2 服务器登录信息
#### 2.2.1 EVE-NG Linux 登录信息:
# 这台Linux只是作为一个跳板机器使用。并<font color=red>不是</font>做实验用的Linux 设备

IP | port| protocol
---|----|----
10.74.82.244|22|SSH
10.74.82.253|22|SSH

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

#### 2.2.2 web登录信息:

IP | port| protocol| username| password
---|---- |---------|---------|---------  
10.74.82.244|80|http|netdevops|netdevops
10.74.82.253|80|http|netdevops|netdevops

#### 2.2.3 登录到模拟的网络设备
Console 登录：

```
telnet 10.74.82.224 <network device's port>
or
telnet 10.74.82.253 <network device's port>
```
Port 信息的获取：

 - 1. 通过 web登录后获取。
 - 2. 见设备信息文件。
 
SSH 登录设备：

#### 1. 先登录到Linux服务器，然后在登录到每台设备。
 
```
 ssh -l 10.74.82.244 -p <linux server port>
 or
 ssh -l 10.74.82.253 -p <linux server port>
 
 然后
 ssh <network device IP>
```
   - \<linux server port > 见设备设备信息文件。默认为root
   - \<network device port> 见设备IP地址分配文件。

Linux Server Name | Protocol |Port | Username | password
------------------|----------|-----|-----|---------
MGT_Linux24       | SSH      |2224 | root     | eve@123
MGT_Linux25       | SSH      |2225 | root     | eve@123
MGT_Linux26       | SSH      |2226 | root     | eve@123
MGT_Linux27       | SSH      |2227 | root     | eve@123
MGT_Linux28       | SSH      |2228 | root     | eve@123
MGT_Linux29       | SSH      |2229 | root     | eve@123
MGT_Linux30       | SSH      |2230 | root     | eve@123
MGT_Linux31       | SSH      |2231 | root     | eve@123
MGT_Linux32       | SSH      |2232 | root     | eve@123
MGT_Linux33       | SSH      |2233 | root     | eve@123

  
#### 2. 通过SSH命令直接登录到网络设备.
<font color=red>可以忽略这部分</font>

 ```
 ssh -J MGT_Linux -l <username> <Device IP>
 ```
   - -J MGT_Linux 为SSH跳板. 我们可以在mac的本地配置ssh的配置文件。

 ```
    MAC 中ssh client 的配置文件为：
    
    Host MGT_Linux
         Hostname 10.74.82.244
         User  root
         Port  2224
 ```

  

### 2.3 Cisco Internal GitHub(Enterprise version) 
# **两台服务器共用<font color=red>一台</font>gitlab**
# <font color=red>所有的文档和代码都在这里。</font>
可以使用CEC账号登录。也可以不登录。

地址为：
[Cisco github] (https://wwwin-github.cisco.com)

项目仓库为：
https://wwwin-github.cisco.com/ChinaSE/netdevops-training/


## 3.0 Jupyter notebook
### 3.1 启动Jupyter notebook server
所有Linux服务器默认都已经启动了 Jupyter notebook server

### 3.2 连接到Jupyter notebook server

Linux Server Name | Protocol |Port | password
------------------|----------|-----|-----
MGT_Linux24       | HTTP      |8824 |  lab123
MGT_Linux25       | HTTP      |8825 |  lab123
MGT_Linux26       | HTTP      |8826 |  lab123
MGT_Linux27       | HTTP      |8827 |  lab123
MGT_Linux28       | HTTP      |8828 |  lab123
MGT_Linux29       | HTTP      |8829 |  lab123
MGT_Linux30       | HTTP      |8830 |  lab123
MGT_Linux31       | HTTP      |8831 |  lab123
MGT_Linux32       | HTTP      |8832 |  lab123
MGT_Linux33       | HTTP      |8833 |  lab123


## 4.0 yang-explorer
所有Linux服务器默认都已经启动了yang-explorer

Linux Server Name | Protocol |Port | username|password
------------------|----------|-----|-----|---------
MGT_Linux24       | HTTP      |8024 | guest | guest
MGT_Linux25       | HTTP      |8025 |  guest | guest
MGT_Linux26       | HTTP      |8026 |  guest | guest
MGT_Linux27       | HTTP      |8027 |  guest | guest
MGT_Linux28       | HTTP      |8028 |  guest | guest
MGT_Linux29       | HTTP      |8029 |  guest | guest
MGT_Linux30       | HTTP      |8030 |  guest | guest
MGT_Linux31       | HTTP      |8031 |  guest | guest
MGT_Linux32       | HTTP      |8032 |  guest | guest
MGT_Linux33       | HTTP      |8033 |  guest | guest 



 
 
 




