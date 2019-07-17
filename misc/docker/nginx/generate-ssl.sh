#!/bin/bash
PREFIX="/etc/letsencrypt/live"
DOMAINS=("groganburners.ie" "groganburners.com")
for i in "${DOMAINS[@]}"
do
	FULL_DIR="$PREFIX"/"$i"
	sudo mkdir -p "$FULL_DIR"
	sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$FULL_DIR"/privkey.pem -out "$FULL_DIR"/fullchain.pem
done

sudo mkdir -p /etc/ssl/certs/
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
