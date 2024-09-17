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
cp -r $SCRIPT_DIR/../* /opt/sjoel
mkdir -p /var/log/sjoelserver

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

# Create user and set permissions
useradd --system --no-create-home sjoeluser
chown -R sjoeluser:sjoeluser /opt/sjoel
chown -R sjoeluser:sjoeluser /var/log/sjoelserver
usermod -a -G video sjoeluser

# Set up wifi hotspot service, needs to run on next startup doesnt work in packer
cp /opt/sjoel/install/setup_wifi.service /etc/systemd/system/
cp /opt/sjoel/install/setup_wifi.sh /usr/local/bin/
chmod +x /usr/local/bin/setup_wifi.sh
systemctl enable setup_wifi.service 2>>/var/log/sjoel_install.log

# Install service
cp /opt/sjoel/install/sjoel.service /etc/systemd/system/
systemctl enable pigpiod.service 2>>/var/log/sjoel_install.log
systemctl enable sjoel.service 2>>/var/log/sjoel_install.log
cat /var/log/sjoel_install.log