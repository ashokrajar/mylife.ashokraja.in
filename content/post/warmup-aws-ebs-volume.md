+++
date = "2017-04-06T22:00:41+05:30"
tags = ["Linux", "AWS", "EBS", "EBS Snapshot", "Volumes", "Warmup"]
description = "Why warming up EBS volumes restored from snaphot is so important for your application"
title = "Warming up AWS EBS volumes restored from Snaphot"
categories = ["Technology", "Cloud", "Storage", "Cloud Computing", "Cloud Storage"]
highlight = "true"
+++

This post talks about the need of pre-waring the EBS volumes...
<!--more-->

## Should we pre-warm/initialize a EBS volume ?

### Newer EBS volumes

Newly provisioned EBS volumes doesn't require a pre-warming and they can attain it's maximum performance from the moment they are available.


### EBS volumes created from Snapshot

EBS volumes created from snapshots need to be pre-warmed/initialized before it can be used on high IO demanding applications.


#### Why ?

* Snapshots are nothing but storage blocks backuped into S3.
* When an EBS volume is created from a snapshot, not all the storage blocks are written in to the volume.
* So when an application tries to read the data (storage block), 
  1. The correspoding storage block are first pulled down from S3 and written to the volume.
  2. Only then it's available for the application to consume the block, and hence increases the latency of an I/O operation the first time each block is accessed


### How to pre-warm/initialize the EBS volume

Using `dd` or `fio` utilities read all the blocks on the volume. The dd command is installed by default in most of the OS, but fio is faster due to it's capability of multi-threaded reads.

#### Using `dd`: (slower)

```
sudo dd if=/dev/xvdf of=/dev/null bs=1M
```

#### Using `fio`: (Considerably faster)

```
sudo fio --filename=/dev/xvdf --rw=read --bs=128k --iodepth=32 --ioengine=libaio --direct=1 --name=volume-initialize
```

{{< hl-text blue >}}
Tip: It took me 12hours to pre-warm a 2TB EBS volume with `fio` utilitly.
{{< /hl-text >}}
