# Case 5  EXABGP

[exabgp source code](https://github.com/Exa-Networks/exabgp)

[exabgp documents](https://github.com/Exa-Networks/exabgp/wiki/_pages)

There are three task in this case:
- use exabgp make a bgp peer
- use exabgp send a ipv4 route
- collect BGP-LS routes

## 1.1 base infomations
eve1(10.74.82.244): 

hostname | Port | username | password    | type
---------|------|----------|-------------| ---
VRR-Linux22    | 33302| root    | eve@123| console
VRR-Linux23    | 33303| root    | eve@123| console


eve2(10.74.82.253):

hostname | Port | username | password    | type
---------|------|----------|-------------| ---
VRR-Linux22    | 33046 | root    | eve@123|console
VRR-Linux23    | 33047 | root    | eve@123|console

VRR-Linux MGT_IP on eve1 and eve2:

hostname      | interface name | IP           | type
--------------| ---------------|--------------| ----
VRR-Linux22|eth0                | 172.20.3.122 | mgt
VRR-Linux23|eth0                | 172.20.3.123 | mgt

VRR-Linux eth1 ip address on eve1 and eve2

hostname      | interface name | IP address
--------------|----------------|--------------
VRR-Linux22   | eth1           | 99.1.2.26/30
VRR-Linux23   | eth1           | 99.1.4.26/30


## 1.2 VRR-Linux Console login

```
telnet 172.20.0.1 33302

```

## 1.2 modify the Linux eth0 and eth1 ip address

### 1.2.1 modify the config file
```
# vi /etc/network/interfaces

#iface eth0 inet dhcp
iface eth0 inet static
      address 172.20.3.122
      netmask 255.255.0.0
      gateway 172.20.0.1
      dns-nameserver 64.104.123.245

iface eth1 inet static
      address 99.1.2.26
      netmask 255.255.255.252
      up route add -net 99.1.0.0 netmask 255.255.0.0  gw 99.1.2.25 dev eth1

```
### 1.2.2 restart the service 
restart the network service and up the interfaces

```
# ip addr flush eth0 && ip addr flush eth1 && systemctl restart networking
```

### 1.2.3 check the ip and the RIB

```
# ip addr | grep -E "eth[0-1]|inet "

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 172.20.3.122/16 brd 172.20.255.255 scope global eth0
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 99.1.2.26/30 brd 99.1.2.27 scope global eth1

# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.20.0.1      0.0.0.0         UG    0      0        0 eth0
99.1.0.0        99.1.2.25       255.255.0.0     UG    0      0        0 eth1
99.1.2.24       0.0.0.0         255.255.255.252 U     0      0        0 eth1
172.20.0.0      0.0.0.0         255.255.0.0     U     0      0        0 eth0
# ping  99.1.2.25 -c 2

PING 99.1.2.25 (99.1.2.25) 56(84) bytes of data.
64 bytes from 99.1.2.25: icmp_seq=1 ttl=255 time=1.77 ms
64 bytes from 99.1.2.25: icmp_seq=2 ttl=255 time=1.30 ms

--- 99.1.2.25 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.308/1.539/1.771/0.234 ms

# ping 99.1.0.1 -c 2

```

### 1.2.4 Login the VRR-Linux Server and run exabgp

- Logout from console

- ssh login 

### 1.2.5 start the py3 venv

```
root@ubuntu:~# source py3/bin/activate
(py3) root@ubuntu:~#

```

### 1.2.6 try the exabgp tools

```
(py3) root@ubuntu:~# exabgp --version
ExaBGP : 4.0.8-793a2931
Python : 3.5.2 (default, Nov 23 2017, 16:37:01)  [GCC 5.4.0 20160609]
Uname  : Linux ubuntu 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64
Root   : /root/py3
```

## Task 1: exabgp to make a bgp peer

### 1.1 check iosxr bgp peer

```
for x in {101..115}; do sshpass -p admin ssh -l admin 172.20.3.${x} show bgp summary | grep -E "99\.1\.[2|4]\.26"; done

```

### 1.2 start an exabgp instance

Create an exabgp config file(exabgp.ini):

```
# Well-Known communtites
# no-export    -  65535:65281  # do not advertise to any eBGP peers
# no-advertise -  65535:65282  # do not advertise to any BGP peer
# local-as     -  65535:65283  # do not advertise this route to peers outside the local as



template {
    neighbor ibgp {
        router-id 99.1.0.9;
        local-address 99.1.2.26;
        local-as 100;
        peer-as  100;
        hold-time 180;


        static {
            route 1.0.0.0/8  next-hop 99.1.2.26 community 65535:65282;
        }
    }
}

neighbor 99.1.0.1 {
     inherit ibgp;
     description "to xrv1 BGP peer";
}

neighbor 99.1.0.2 {
     inherit ibgp;
     description "to xrv2 BGP peer";
}

neighbor 99.1.0.3 {
     inherit ibgp;
     description "to xrv3 BGP peer";
}

neighbor 99.1.0.4 {
     inherit ibgp;
     description "to xrv4 BGP peer";
}

neighbor 99.1.0.5 {
     inherit ibgp;
     description "to xrv5 BGP peer";
}

neighbor 99.1.0.6 {
     inherit ibgp;
     description "to xrv6 BGP peer";
}

neighbor 99.1.0.7 {
     inherit ibgp;
     description "to xrv7 BGP peer";
}


```

### 1.3 check route on the exabgp routers

```
a)show bgp summary:

RP/0/0/CPU0:xrv2#show bgp summary
Mon Aug 27 09:06:11.441 UTC
BGP router identifier 99.1.0.2, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 3
BGP main routing table version 3
BGP NSR Initial initsync version 2 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

BGP is operating in STANDALONE mode.


Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
Speaker               3          3          3          3           3           0

Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
99.1.0.1          0   100   23290   23286        3    0    0     2w2d          0
99.1.0.3          0   100   23294   23288        3    0    0     2w2d          0
99.1.0.4          0   100   23288   23288        3    0    0     2w2d          0
99.1.0.5          0   100   23288   23282        3    0    0     2w2d          0
99.1.0.6          0   100   23288   23283        3    0    0     2w2d          0
99.1.0.7          0   100   23282   23283        3    0    0     2w2d          0
99.1.0.8          0   100   23289   23283        3    0    0     2w2d          0
99.1.2.26         0   100       6       5        3    0    0 00:02:35          1


b)show bgp route 1.0.0.0/8 detail

RP/0/0/CPU0:xrv1#show bgp 1.0.0.0/8 detail
Mon Aug 27 09:14:57.895 UTC
BGP routing table entry for 1.0.0.0/8
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                  3           3
    Flags: 0x00001001+0x00000000;
Last Modified: Aug 27 09:13:24.606 for 00:01:33
Paths: (1 available, best #1, not advertised to any peer)
  Not advertised to any peer
  Path #1: Received by speaker 0
  Flags: 0x4000000001040207, import: 0x20
  Not advertised to any peer
  Local, (Received from a RR-client)
    99.1.2.26 from 99.1.2.26 (99.1.0.9)
      Origin IGP, localpref 100, valid, internal, best, group-best
      Received Path ID 0, Local Path ID 1, version 3
      Community: no-advertise

```




IOSXR BGP config:

```
RP/0/0/CPU0:xrv1# show run router bgp
Mon Aug 27 12:58:32.197 UTC
router bgp 100
 address-family ipv4 unicast
 !
 address-family link-state link-state
 !
 address-family ipv4 sr-policy
 !
 neighbor 99.1.0.2
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.0.3
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.0.4
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.0.5
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.0.6
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.0.7
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.0.8
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
 neighbor 99.1.2.26
  remote-as 100
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
  address-family link-state link-state
  !
  address-family ipv4 sr-policy
   route-reflector-client
  !
 !
!



```