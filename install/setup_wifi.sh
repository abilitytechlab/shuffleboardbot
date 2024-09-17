#!/bin/bash

# Add Wi-Fi AP configuration
nmcli connection add type wifi con-name "Hotspot" autoconnect yes wifi.mode ap wifi.ssid "Sjoelbak" ipv4.method shared ipv6.method shared
nmcli con up Hotspot


# Disable the service after running
systemctl disable setup_wifi.service

