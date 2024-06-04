#!/bin/bash
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

# Install service
cp sjoel.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable sjoel.service
systemctl start sjoel.service