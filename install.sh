#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Create directories and copy files
mkdir /opt/sjoel
cp -r . /opt/sjoel
cd /opt/sjoel
mkdir -p /var/log/sjoelserver

# Create user and set permissions
useradd --system --no-create-home sjoeluser
chown -R sjoeluser:sjoeluser /opt/sjoel
chown -R sjoeluser:sjoeluser /var/log/sjoelserver

# Install dependencies
add-apt-repository ppa:deadsnakes/ppa 
apt-get update
apt-get install python3.11 pigpio python-pigpio python3-pigpio

# Create venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Set up wifi hotspot
nmcli con add type wifi ifname wlan0 con-name Hotspot autoconnect yes ssid Sjoelbak
nmcli con modify Hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify Hotspot wifi-sec.key-mgmt wpa-psk
nmcli con modify Hotspot wifi-sec.psk "LekkerSjoelen123"
nmcli con modify Hotspot connection.autoconnect true
nmcli con up Hotspot

# Install service
cp sjoel.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable sjoel.service
systemctl start sjoel.service