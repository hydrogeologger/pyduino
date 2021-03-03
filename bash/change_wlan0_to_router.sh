#!/bin/bash
# reference: https://github.com/hydrogeologger/pyduino/wiki/Making-Raspberry-Pi-as-an-internet-Router-(NAT)

apt-get install dnsmasq hostapd

if [ -f /etc/dhcpcd.conf ]; then
    cp  /etc/dhcpcd.conf  /etc/dhcpcd_orig.conf   # note this needs to be copied and also work for the first time when we do the config
fi


cat <<EOT >> /etc/dhcpcd.conf
interface wlan0
    static ip_address=192.168.4.1/24
EOT


if [ -f /etc/dnsmasq.conf ]; then
    mv  /etc/dnsmasq.conf  /etc/dnsmasq_orig.conf
fi


cat <<EOT >> /etc/dnsmasq.conf
interface=wlan0      # Use the require wireless interface - usually wlan0
  dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOT




if [ -f /etc/hostapd/hostapd.conf ]; then
    mv  /etc/hostapd/hostapd.conf  /etc/hostapd/hostapd_orig.conf
fi



cat <<EOT >> /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=sa1
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=uqgec
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOT




if [ -f /etc/default/hostapd ]; then
    mv  /etc/default/hostapd /etc/default/hostapd_orig
fi



cat <<EOT >> /etc/default/hostapd
DAEMON_CONF="/etc/hostapd/hostapd.conf"
EOT

systemctl unmask hostapd
systemctl unmask dnsmasq

systemctl enable hostapd
systemctl enable dnsmasq
