#!/bin/sh
apt install linux-headers-amd64
deb http://deb.debian.org/debian/ sid main contrib non-free non-free-firmware
apt update
apt install firmware-misc-nonfree
apt install nvidia-tesla-450-driver
