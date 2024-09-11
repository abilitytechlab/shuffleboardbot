#!/bin/bash

# Add Wi-Fi AP configuration
nmcli con add type wifi ifname wlan0 con-name Hotspot autoconnect yes ssid Sjoelbak
nmcli con modify Hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify Hotspot wifi-sec.key-mgmt wpa-psk
nmcli con modify Hotspot wifi-sec.psk "LekkerSjoelen123"
nmcli con modify Hotspot connection.autoconnect true
nmcli con up Hotspot

# Disable the service after running
systemctl disable setup_wifi.service