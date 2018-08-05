# TODO LIST

## 1.0 lab base informations

- [ ] login lab
  - [x] mac osx
  - [ ] windows 10
- [ ] customize img
  - [x] vIOS
  - [x] xrvr
  - [ ] Linux 
     - [ ] python3 venv
     - [ ] python packages
         - pexpect
         - netmiko
         - networkx
         - netaddr
         - exabgp
         - jinja2
         - requests
         - flask
         - ncclient
         - pyaml
         - lxml
         - textfsm          
     - [ ] jupyter server
     - [ ] yang-explorer
     - [ ] set screen
     - [x] git
     - [x] set proxy
  
- [ ] lab base infomations
    - config templates
      - [x] SSH Server config
      - [x] interface/mgt
      - [x] lldp
      - [x] hostname
      - protocol (IGP/BGP)
         - [ ] ISIS
         - [ ] BGP
         - [ ] Segement Routing
      - [ ] MPLS VPN
- [x] assign ip address in the topology/make a csv file and markdown file
   - mgt interface and ipaddress
   - interconnect ip address 

## 2.0 docs 
- [x] customzie eve img
- [x] make a training topology

## 3.0 LABS

### 3.1 CASE 1: use telnet and ssh login the network device

 - init config (telnet console)
    - set hostname 
    - enable ssh server
    - mgt ip address
    - lldp enable
 - config device (netmiko)
    - interface ip address config 
    - isis config
    - sr config
    - bgp config
    - netconf
    
### 3.2 CASE 2: use AsyncIO to backup the device configure 
 - pexpect asyncIO

### 3.3 CASE 3: use netconf get lldp and isis topology
 - get lldp neighbor
 - get isis topology

### 3.4 CASE4: use yang-exporler to get network device infos
 - how to use yang-expoler

### 3.5 CASE5: use exabgp to manage the bgp routes
 - exabgp to make a bgp peer
 - exabgp to send a ipv4 route
 - collect BGP-LS routes
 
### 3.6 CASE6: use RestAPI with XTC
 - use case 5's BGP-LS informations to compute a path
 - send a SR-Policy to device
 



