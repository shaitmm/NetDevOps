# Case 5  EXABGP

[exabgp source code](https://github.com/Exa-Networks/exabgp)

[exabgp documents](https://github.com/Exa-Networks/exabgp/wiki/_pages)

There are three task in this case:
- use exabgp make a bgp peer
- use exabgp send a ipv4 route
- collect BGP-LS routes



## Task 3: collect BGP-LS routes


### 1.1 create a new exabgp config file

exabgp_ls.ini

```
template {
    neighbor ibgp {
        router-id 99.1.0.9;
        local-address 99.1.2.26;
        local-as 100;
        peer-as  100;
        hold-time 180;
    }
}

process bgp_ls {
        run ./bgp_ls.py;
        encoder json;
}

neighbor 99.1.0.1 {
     family {
          bgp-ls bgp-ls;
     }
     api {
       processes [ bgp_ls ];
       receive {
              parsed;
              update;
       }

     }
     inherit ibgp;
}

```

### 1.2 write the  python code

filename: bgp_ls.py

```
#!/usr/bin/env python

import sys
import os
import time
import json

f = open("/root/exabgp/test.log", "a+")

while True:
    line = sys.stdin.readline().strip()
    if line and "exabgp" in line:
        f.write(line + "\n" )
        f.flush()

```
**change the rest_api.py file execute attrib**


```
chmod +x bgp_ls.py

ls -l bgp_ls.py
-rwxr-xr-x 1 root root 244 Aug 27 20:44 bgp_ls.py

```

### 1.3 set iosxr config

```
isis config:

router isis lab
  distribute link-state level 2
   
bgp config:

router bgp 100
  address-family link-state link-state
  neighbor 99.1.2.26
  remote-as 100
  update-source Loopback0
  
  address-family link-state link-state
```

### 1.3 start the exabgp service
```
 env exabgp.daemon.user=root exabgp exabgp_ls.ini
21:13:15 | 13897  | welcome       | Thank you for using ExaBGP
21:13:15 | 13897  | version       | 4.0.8-793a2931
21:13:15 | 13897  | interpreter   | 3.5.2 (default, Nov 23 2017, 16:37:01)  [GCC 5.4.0 20160609]
21:13:15 | 13897  | os            | Linux ubuntu 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64
21:13:15 | 13897  | installation  | /root/py3
21:13:15 | 13897  | advice        | environment file missing
21:13:15 | 13897  | advice        | generate it using "exabgp --fi > /root/py3/etc/exabgp/exabgp.env"
21:13:15 | 13897  | cli           | could not find the named pipes (exabgp.in and exabgp.out) required for the cli
21:13:15 | 13897  | cli           | we scanned the following folders (the number is your PID):
21:13:15 | 13897  | cli control   |  - /run/exabgp/
21:13:15 | 13897  | cli control   |  - /run/0/
21:13:15 | 13897  | cli control   |  - /run/
21:13:15 | 13897  | cli control   |  - /var/run/exabgp/
21:13:15 | 13897  | cli control   |  - /var/run/0/
21:13:15 | 13897  | cli control   |  - /var/run/
21:13:15 | 13897  | cli control   |  - /root/py3/run/exabgp/
21:13:15 | 13897  | cli control   |  - /root/py3/run/0/
21:13:15 | 13897  | cli control   |  - /root/py3/run/
21:13:15 | 13897  | cli control   |  - /root/py3/var/run/exabgp/
21:13:15 | 13897  | cli control   |  - /root/py3/var/run/0/
21:13:15 | 13897  | cli control   |  - /root/py3/var/run/
21:13:15 | 13897  | cli control   | please make them in one of the folder with the following commands:
21:13:15 | 13897  | cli control   | > mkfifo /root/exabgp/run/exabgp.{in,out}
21:13:15 | 13897  | cli control   | > chmod 600 /root/exabgp/run/exabgp.{in,out}
21:13:15 | 13897  | configuration | performing reload of exabgp 4.0.8-793a2931
21:13:15 | 13897  | reactor       | loaded new configuration successfully
21:13:15 | 13897  | reactor       | connected to peer-1 with outgoing-1 99.1.2.26-99.1.0.1

```

#### **env exabgp.daemon.user=root** must be used when you login by root


### 1.4 check the bgp linkstate log
```
cat test.log
```

Each line in this log file is json format text. so you can copy it in the firefox. 
Firefox can parse this json format.


