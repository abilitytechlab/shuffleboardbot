#!/bin/bash

# Add Wi-Fi AP configuration
nmcli connection add type wifi con-name "TestBoris" autoconnect yes wifi.mode ap wifi.ssid "Borisss" ipv4.method shared ipv6.method shared
nmcli con up Hotspot


# Disable the service after running
systemctl disable setup_wifi.service

