---
title: "Building a Micro Datacenter at Home"
date: 2021-03-28T00:59:09+04:00
categories:
- Data Center
- Home Data Center
- DIY Data Center
- Virtual Machines
tags:
- DataCenter
- Home DataCenter
- Virtualbox
- Proxmox
- Raspberry PI
- ARM
- x86
keywords:
- DataCenter
- Micro DataCenter
- Home DataCenter
- Virtualbox
- Proxmox
- Raspberry PI
- ARM
- x86
- PI4
thumbnailImage: "/img/thumbs/home-dc-architecture.png"
---

Creating a mini Data Center at home has been my long term dream. Since my ISP gave me a static IP very cheap and finally was able to spend some $$$ to afford it and most importantly got some time to set it up.
<!--more-->
# Architecture

![](/img/home-dc-architecture.png)

# Hardware
### *1 x emini NUC Mini PC — Metal01*
*Compute : i7 8th Gen 8750H (6 Core), 9M Cache, 2.2GHz upto 4.1GHz Turbo*   
*Memory : 32GB RAM*  
*Storage : 1 TB HDD, 1TB Software RAID1 (2 x SSD USB3), 2 x 5TB usb HDD, 1 x 2TB usb HDD*  

### *1 x emini NUC Mini PC — Metal02*  
*Compute : i7 8th Gen 8750H (6 Core), 9M Cache, 2.2GHz upto 4.1GHz Turbo*    
*Memory : 32GB RAM*   
*Storage : 1 TB HDD, 1TB Software RAID1 (2 x SSD USB3)*   

### *1 x Raspberry Pi 4 — Atom*  
*Compute : Quad core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz*   
*Memory : 4GB RAM*  
*Storage : 32GB MicroSD, 1 x 5TB Segate Portable HDD, 1 x 4TB Segate Portale HDD*  

### *1 x Apple Mac Mini — Main PC*
*Compute : 6-core Intel Core i7, 12MB shared L3 cache, 3.2GHz upto 4.6GHz Turbo*   
*Memory : 32GB RAM*  
*Storage : 1 TB SSD, 1 x 2TB NVMe SSD*  
*Keyboard : [Keychron K2](https://www.keychron.com/products/keychron-k2-wireless-mechanical-keyboard)*  
*Mouse : [Logitech MX Master 3](https://www.logitech.com/en-us/products/mice/mx-master-3.910-005620.html)*  

### *Network : 1 x 8 Port Gigabit Switch*
### *Router : 1 x Asus 5ghz Gigabit Router*

# Infra Setup

### Router, Switch and Raspberry Pi 4

![](/img/router-switch-pi4.png)

### Metal01 & Metal02

![](/img/metal01-02.png)

### Main PC, Monitor & GPU

![](/img/main-pc.png)

# Alright What I use it for ??

I use this for various purpose. Learning, Experimenting new technology & POCs, Media storage & Streaming 4K videos to Android and Apple TV, Backups etc..

### *Metal01 — Core VMs*  
- cmdcenter — a bastion server, Haproxy server to expose some internal service like (VS Code Server, Proxmox KVM UI, Firefly III UI etc)
- Core K8 Cluster — Running Firefly III (Personal Finance Manager)
- Windows 10 — Once in a while need this for some odd reasons
- NAS Server VM — All the storage is connected to this VM and shared via Samba, NFS, AFP.

### *Metal02 — Other VMs*
- Experimental K8 Cluster
- clitools — Multiuser env with all the cloud cli tools installed
- Few other POC VMs

### *Atom*
- [Deluged](https://dev.deluge-torrent.org) Torrent Client with a WebUI
- [Plex Media Server](https://www.plex.tv/media-server-downloads/)
- TimeMachine Server

### *Main PC*
This is my main computer I use daily for all things(Writing Code, Mail, Teams, Slack, Browsing, Editing Pictures I shoot, Writing this Blog etc)

- [VS Code Server](https://github.com/cdr/code-server) (Web IDE based on Microsoft VS Code)
- Docker Desktop
- All the IDEs Installed. (VSCode, VIM, EMacs, IntelliJ(Idea, Goland, Pycharm, WebStorm), XCode)
- All developer tools and languages Installed
- All messaging and meeting applications
- Various browsers. Though Safari and [Vivaldi](https://vivaldi.com) are my browser of choice.
- Lightroom CC, Photoshop CC
