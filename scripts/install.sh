#!/bin/bash
wg genkey | tee private.key | wg pubkey > public.key
sed -i "s|<GENERATE_ON_INSTALL>|$(cat private.key)|" configs/wg0.conf
sudo cp configs/wg0.conf /etc/wireguard/wg0.conf
sudo wg-quick up wg0
echo "Y-God live. Bloom active."
