# Case 5  EXABGP

[exabgp source code](https://github.com/Exa-Networks/exabgp)

[exabgp documents](https://github.com/Exa-Networks/exabgp/wiki/_pages)

There are three task in this case:
- use exabgp make a bgp peer
- use exabgp send a ipv4 route
- collect BGP-LS routes



## Task 2: exabgp send an ipv4 route by rest API

### 1.1 create a new exabgp config file

exabgp_api.ini

```
# Well-Known communtites
# no-export    -  65535:65281  # do not advertise to any eBGP peers
# no-advertise -  65535:65282  # do not advertise to any BGP peer
# local-as     -  65535:65283  # do not advertise this route to peers outside the local as

process rest_api {
     run ./rest_api.py;
     encoder json;
 }


template {
    neighbor ibgp {
        router-id 99.1.0.9;
        local-address 99.1.2.26;
        local-as 100;
        peer-as  100;
        hold-time 180;
       
        api {
            processes [ rest_api ];
            neighbor-changes;
            send {
                packets;
            }
        }

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

### 1.2 write the rest API python code

filename: rest_api.py

```
#!/usr/bin/env python

from flask import Flask, request
from sys import stdout


app = Flask(__name__)

@app.route("/", methods=["POST"])
def command():
    command = request.form["command"]
    if "65535:65282" not in command and "announce route" in command :
        command = command + " community 65535:65282"
    stdout.write("%s\n" %command)
    stdout.flush()

    return "%s\n" %command

if __name__ == "__main__":
    app.run()

```
**change the rest_api.py file execute attrib**

The rest API port is TCP: 5000

```
chmod +x rest_api.py

ls -l rest_api.py
-rwxr-xr-x 1 root root 438 Aug 27 17:52 rest_api.py
```


### 1.3 start the exabgp service with rest api
```
env exabgp.daemon.user=root exabgp exabgp_api.ini

18:03:40 | 13058  | welcome       | Thank you for using ExaBGP
18:03:40 | 13058  | version       | 4.0.8-793a2931
18:03:40 | 13058  | interpreter   | 3.5.2 (default, Nov 23 2017, 16:37:01)  [GCC 5.4.0 20160609]
18:03:40 | 13058  | os            | Linux ubuntu 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64
18:03:40 | 13058  | installation  | /root/py3
18:03:40 | 13058  | advice        | environment file missing
18:03:40 | 13058  | advice        | generate it using "exabgp --fi > /root/py3/etc/exabgp/exabgp.env"
18:03:40 | 13058  | cli           | could not find the named pipes (exabgp.in and exabgp.out) required for the cli
18:03:40 | 13058  | cli           | we scanned the following folders (the number is your PID):
18:03:40 | 13058  | cli control   |  - /run/exabgp/
18:03:40 | 13058  | cli control   |  - /run/0/
18:03:40 | 13058  | cli control   |  - /run/
18:03:40 | 13058  | cli control   |  - /var/run/exabgp/
18:03:40 | 13058  | cli control   |  - /var/run/0/
18:03:40 | 13058  | cli control   |  - /var/run/
18:03:40 | 13058  | cli control   |  - /root/py3/run/exabgp/
18:03:40 | 13058  | cli control   |  - /root/py3/run/0/
18:03:40 | 13058  | cli control   |  - /root/py3/run/
18:03:40 | 13058  | cli control   |  - /root/py3/var/run/exabgp/
18:03:40 | 13058  | cli control   |  - /root/py3/var/run/0/
18:03:40 | 13058  | cli control   |  - /root/py3/var/run/
18:03:40 | 13058  | cli control   | please make them in one of the folder with the following commands:
18:03:40 | 13058  | cli control   | > mkfifo /root/exabgp/run/exabgp.{in,out}
18:03:40 | 13058  | cli control   | > chmod 600 /root/exabgp/run/exabgp.{in,out}
18:03:40 | 13058  | configuration | performing reload of exabgp 4.0.8-793a2931
18:03:40 | 13058  | reactor       | loaded new configuration successfully
18:03:40 | 13058  | reactor       | connected to peer-4 with outgoing-2 99.1.2.26-99.1.0.4
18:03:40 | 13058  | reactor       | connected to peer-5 with outgoing-3 99.1.2.26-99.1.0.5
18:03:40 | 13058  | reactor       | connected to peer-2 with outgoing-4 99.1.2.26-99.1.0.2
18:03:40 | 13058  | reactor       | connected to peer-3 with outgoing-5 99.1.2.26-99.1.0.3
18:03:40 | 13058  | reactor       | connected to peer-7 with outgoing-6 99.1.2.26-99.1.0.7
18:03:40 | 13058  | reactor       | connected to peer-6 with outgoing-7 99.1.2.26-99.1.0.6
18:03:40 | 13058  | reactor       | connected to peer-1 with outgoing-1 99.1.2.26-99.1.0.1
18:03:40 | 13058  | api           | command from process not understood : * Serving Flask app "rest_api" ( lazy loading )
18:03:40 | 13058  | api           | command from process not understood : * Environment: production
18:03:40 | 13058  | api           | command from process not understood : WARNING: Do not use the development server in a production environment.
18:03:40 | 13058  | api           | command from process not understood : Use a production WSGI server instead.
18:03:40 | 13058  | api           | command from process not understood : * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

#### **env exabgp.daemon.user=root** must be used when you login by root


### 1.4 use curl call the rest api

#### a) announce a route
```
# curl --form "command=neighbor 99.1.0.1 announce route 100.1.1.0/24 next-hop 99.1.0.2" http://localhost:5000

api return message:
neighbor 99.1.0.1 announce route 100.1.1.0/24 next-hop 99.1.0.2 community 65535:65282
```
#### b) withdraw a route

```
curl --form "command=neighbor 99.1.0.1 withdraw route 100.1.1.0/24 next-hop 99.1.0.2" http://localhost:5000


API return:
neighbor 99.1.0.1 withdraw route 100.1.1.0/24 next-hop 99.1.0.2
```

Reference:
https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-interacting-from-the-API


