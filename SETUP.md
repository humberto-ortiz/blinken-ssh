# Setting up kali on Raspberry Pi 3 for cyber-camp

## Introduction

For our cyber-camp, students will use kali linux on Raspberry
Pi 3. The default RPi images need some tweaking, here's what I did to
configure mine.

## Methods

Follow the
[installation instructions](http://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi)
to make an SD card to boot kali.

The stock image is an 8GB partition, and our cards are 16 GB, so half
the card is unallocated. Install gparted, and expand the partition to
fill the card.

```
$ apt install gparted
$ gparted
```

The default image is a minimal install, install the rest of the kali
linux tools.

```
$ apt update
$ apt upgrade
$ apt install kali-linux-full
$ apt install steghide
```

For the sshscan lab, we need a few more python modules.

```
$ apt install python-netaddr
$ pip install RPi.GPIO
```

Now you can clone the lab scripts.

```
$ cd Documents
$ git clone https://github.com/humberto-ortiz/blinken-ssh.git
$ git clone https://github.com/humberto-ortiz/scripts-n-tools.git
```

## Results

You should now have a working kali linux image you can use for cyber-camp.
