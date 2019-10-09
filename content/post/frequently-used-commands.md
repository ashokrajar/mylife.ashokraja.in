+++
description = "Commands I use very freqently on my daily job"
tags = ["Linux", "MacOS", "FrequentlyUsedCommands", "Hacks"]
date = "2016-11-07T09:45:20+05:30"
categories = ["Technology", "Frequently Used", "Linux Commands", "Mac Commands", "Hacks"]
title = "Linux/Mac Frequently Used Commands"
highlight = "true"
+++

### Some of the very basic commands I use very freqently on my daily job on my Workstation(MacOS) & on the Remote servers(Linux).

<!--more-->

# AWS
---
##### List all instance-id behind the ELB
```
aws elb describe-load-balancers --output text --load-balancer-names <lb_name> | grep INSTANCES | awk '{print $2}'
```
##### Get all the instances public ip-address behind the ELB
```
aws elb describe-load-balancers --output text --load-balancer-names <lb_name> | grep INSTANCES | awk '{print $2}' | xargs aws ec2 describe-instances --output text --instance-ids | grep INSTANCES | awk '{print $14}'
```

#### Launching instance with a instance-store volumes
```
aws ec2 run-instances --image-id <ami-id> --security-groups <group-name> --instance-type <instance-type> --region <region> --key-name <keypair-name>  --placement AvailabilityZone=us-east-1d --iam-instance-profile Name=<IAM-role-name> --block-device-mappings "[{\"DeviceName\": \"/dev/sdc\",\"VirtualName\":\"ephemeral1\"}]"
```
#### Whitelisting ips
```
aws ec2 authorize-security-group-ingress --group-name <group-name> --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 8000, "ToPort": 8000, "IpRanges": [{"CidrIp": "192.168.10.20/28"}, {"CidrIp": "192.168.20.232/30"}, {"CidrIp": "192.168.10.40/32"}]} ]'
```
#### List all users API key ID
```
for USER in `aws iam list-users --output text | awk '{print $2}' | cut -f2 -d/`; do aws iam list-access-keys --user-name $USER --output text >> iam_user_apikeylist.txt ; done
```

#### Calculating AWS S3 billing report
```
Value / (1024 * 1024 * 1024 * 24)
```
<br>
# Performance Tuning
---
#### Improve disk wire performance by adding these mount option to the /etc/fstab mount options
```
noatime,nodiratime,data=writeback
```
- *noatime* : fully disables writing file access times to the drive every time you read a file
- *nodiratime* : option disables the writing of file access times only for directories. This option is not required as *noatime* implies *nodiratime*
- *data=writeback* : data gets written out long after the metadata hit the disk. Hence improving the performance. **But use it with caution at your own risk as you may loss your recent data if the machine ever goes down**

#### To change live filesystem journaling option
```
tune2fs -O has_journal -o journal_data_writeback <part>
```

#### Enable hashed b-tree to speed up lookups for large directories
```
tune2fs -O dir_index <part>
```
- dir_index : is a hashed b-tree implementation for ext3, it's riskfree and adds a bit of performance to your filesystem.

#### Optimize directories in filesystem
```
e2fsck -D <part>
```
- This option causes e2fsck to try to optimize all directories, either by reindexing them if the filesystem supports directory indexing, or by sorting and compressing directories for smaller directories, or for filesystems using traditional linear directories.

#### System Profiling
```
oprofiled --session-dir=/var/lib/oprofile --separate-lib=1 --separate-kernel=1 --separate-thread=0 --separate-cpu=0 --events= --no-vmlinux
sudo opcontrol --no-vmlinux --separate=kernel
sudo opcontrol --deinit; sudo modprobe oprofile timer=1
sudo opcontrol --reset;sudo opcontrol --start
```
<br>
# VirtualBox
---
#### Configure DHCP
```
VBoxManage dhcpserver add --netname 'intnet01' --ip 10.10.10.254 --netmask 255.255.255.0 --lowerip 10.10.10.10 --upperip 10.10.10.20 --enable
```
#### Restart virtual box in MacOS
```
sudo /Library/StartupItems/VirtualBox/VirtualBox restart
```
<br>
# MacOS
---
#### Disable/Enable swap
```
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.dynamic_pager.plist
sudo rm /private/var/vm/swapfile*
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.dynamic_pager.plist
```
<br>
# SSH Hacks
---
#### Tunneling for SOCKS Proxy
```
ssh -D <localport_number> -f -C -q -N remote.host.address
```
#### Read pub key form a private key
```
ssh-keygen -y -f ~/.ssh/id_rsa
```
#### Tunneling multiple remote services to access locally through a ssh proxy host
```
ssh -L 1080:remote1.host.address:80 -L <local_port>:remote2.host.address:<remote_port>  -L 2222:remote3.host.address:22 user_name@proxy.host.address
```
- To login to remote3.host.address
	```
	ssh -p 2222 localhost
	```

<br>
# OpenSSL
---
#### Creating Self Signed CERT :
```
openssl genrsa -des3 -out server.key 1024
openssl req -new -key server.key -out server.csr
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```
#### Creating CSR
```
mkdir -p /root/CA
openssl genrsa -des3 -out domainname.key 1024
openssl req -new -key domainname.key -out domainname.csr
```
#### Create new revoke list
```
openssl ca -key ca_key.pem -cert ca_crt.pem -gencrl -out ~/ca_crl.pem
```

<br>
# Security
---
#### Iptables : Redirect traffic using
Redirect all traffic to port *80* on interface *eth0* to port *8000*

```
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000
```

#### Iptables : List all NAT rules
```
iptables -t nat -L -n -v
```

#### Iptables : Filter based on string
This rule will filter all the HTTP request based on the uri string given

```
iptables -I INPUT -p tcp --dport 8080 -m string --algo bm --string "status" -j REJECT
```
<br>
# Network
---
#### Validate a list of FQDN
```
for I in $FQDNLIST; do  host $I > /dev/null 2> /dev/null; if [ $? = 0 ]; then echo "$I Yes"; else echo "$I No"; fi; done
```

#### Check if host is alive
```
for I in $HOSTLIST; do  ping -c 2 $I > /dev/null 2> /dev/null; if [ $? = 0 ]; then echo "$I Alive"; else echo "$I Dead"; fi; done
```
<br>
# TCP Dump
---
- *-A* : Print each packet (minus its link level header) in ASCII. Handy for capturing web pages
- *-i* : Listen  on  interface
- *-l* : Make stdout line buffered. Useful if you want to see the data while capturing it
- *-s* : snaplen bytes of data from each packet rather than the default  of  65535 bytes
- *-vvv* : Even more verbose output
- *-w* : Write the raw packets to file rather than parsing and printing them out
- *-x* : When parsing and printing, in addition to printing the headers of each packet, print the data of each packet (minus its link level header) in hex and ASCII. This is very handy for analysing new protocols
- *-X* : When parsing and printing, in addition to printing the headers of each packet, print the data of each packet (minus its link level header) in hex and ASCII.  This is very handy for analysing new protocols
- *-XX* : When parsing and printing, in addition to printing the headers of each packet, print the data of each packet, including its link level header, in hex and ASCII

#### Dump everything on interface *eth0*
tcpdump -s 65535 -i eth0 -w /home/ec2-user/tcpdump.txt

#### View packets on port *8998* only for interface *eth0*
```
tcpdump -l -XXvvv -i eth0 port 8998
```

#### View packets only for a hostname
```
tcpdump -l -XXvvv hostname
```

#### Viewing the complete request
```
tcpdump -vvvs 1500 -l -A host example.com
```

To view only for port 25

```
tcpdump -vv -x -X -s 1500 -i eth1 'port 25'
```
<br>
# Debugging
---
#### Trace a program's system call & signals
```
strace -T -f -o /tmp/strace.out program_to_run
```
- *-T* : Show the time spent in system calls.  This records the time difference between the beginning and the end of each system call
- *-f* : Trace  child  processes  as they are created by currently traced processes as a result of the fork(2), vfork(2) and clone(2) system calls
- *-o* : Store the trace results in a file

<br>
# Bash Hacks
---
#### Creating multiple directory trees
```
sudo mkdir -p cache/0{0..9}/{0..9}{0..9}
sudo mkdir -p cache/0{A..F}/{0..9}{0..9}
sudo mkdir -p cache/0{0..9}/{0..9}{A..F}
sudo mkdir -p cache/0{A..F}/{0..9}{A..F}
sudo mkdir -p cache/0{0..9}/{A..F}{0..9}
sudo mkdir -p cache/0{A..F}/{A..F}{0..9}
sudo mkdir -p cache/0{0..9}/{A..F}{A..F}
sudo mkdir -p cache/0{A..F}/{A..F}{A..F}
sudo chown nobody.wheel cache
sudo chown nobody.nobody cache/* -R
```

#### Recursively display memory usage
```
echo -en "Time\t\tMemUsage(MB)\n~~~~\t\t~~~~~~~~~~~~\n"; while [ 1 ] ; do  stat=`date && free -m | grep "+ buffer"`;echo $AA | awk '{print $4"\t"$9}' ; sleep 60; done
```

#### Deleting a block/multiple-line in a file
```
sed -i '/<plugins plugin="myplugin"/,/<\/plugins>/d' sample.xml
```

#### Extract an RPM package
```
rpm2cpio rpm.rpm | cpio -idmv
```
<br>
# GIT
---
#### Configure global ignore
```
git config --global core.excludesfile ~/.gitignore
```

#### Set username & email
The first thing to do is to set your user name and email address. Every Git commit uses this information, and it’s immutably cooked into your commits.

```
git config --global user.name "Your Name"
git config --global user.email yourmail_id@example.com
```

#### Pull with automatic rebase
Force all new branches to automatically use rebase

```
git config branch.autosetuprebase always
```

Force existing branches to use rebase

```
git config branch.<branch-name>.rebase true
```

#### revert to last commit
```
git reset --soft HEAD~1
```
<br>
# HAProxy
---
#### View haproxy server statisics
```
echo "show table ft_web" | socat unix:./haproxy.stats -
```
<br>
# LOG Parsing
---
#### Occurrence of ipaddresses
```
cat log_file.log | awk '{print $6}' | cut -f1 -d: | sort | uniq -c | awk '{print $1"\t"$2}' | sort -t\t -nrk 1,1
```

#### Empty/Zero a log file without restarting the service which has opened it
```
> /path/to/logfile.log
```