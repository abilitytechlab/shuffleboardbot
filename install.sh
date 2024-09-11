#!/bin/bash -x
set -e
export DEBIAN_FRONTEND="noninteractive"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Script directory: $SCRIPT_DIR"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Create pi user if it does not exist
if id "pi" &>/dev/null; then
  echo "User pi already exists"
else
  useradd -m pi
  usermod -aG sudo pi
fi
echo "pi:raspberry" | chpasswd

# Enable ssh for pi user
mkdir /home/pi/.ssh
touch /home/pi/.ssh/authorized_keys
cat $SCRIPT_DIR/id_rsa.pub >> /home/pi/.ssh/authorized_keys

# Disable password login
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config

# Create directories and copy files
mkdir /opt/sjoel
cp -r $SCRIPT_DIR/ /opt/sjoel
mkdir -p /var/log/sjoelserver

# Create user and set permissions
useradd --system --no-create-home sjoeluser
chown -R sjoeluser:sjoeluser /opt/sjoel
chown -R sjoeluser:sjoeluser /var/log/sjoelserver

# Install dependencies
# apt-get update
# apt-get -y install software-properties-common python3-launchpadlib
# apt-get update
# add-apt-repository ppa:deadsnakes/ppa
# apt-get update
# apt-get -y upgrade
# echo "Installing dependencies"
# apt-get -y install python3.11 pigpio python3-pigpio

# Create venv
python3.11 -m venv /opt/sjoel/venv
source /opt/sjoel/venv/bin/activate
pip install -r /opt/sjoel/requirements.txt
pip install gunicorn

# Set up wifi hotspot
nmcli con add type wifi ifname wlan0 con-name Hotspot autoconnect yes ssid Sjoelbak
nmcli con modify Hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify Hotspot wifi-sec.key-mgmt wpa-psk
nmcli con modify Hotspot wifi-sec.psk "LekkerSjoelen123"
nmcli con modify Hotspot connection.autoconnect true
nmcli con up Hotspot

# Install service
cp /opt/sjoel/sjoel.service /etc/systemd/system/
systemctl enable pigpiod.service
systemctl enable sjoel.service
systemctl daemon-reload