#!/bin/sh

mkdir -p /etc/nginx/ssl/live/${NGINX_HOST}
cp -u /etc/nginx/ssl/live/localhost/fullchain.pem /etc/nginx/ssl/live/${NGINX_HOST}/fullchain.pem
cp -u /etc/nginx/ssl/live/localhost/privkey.pem /etc/nginx/ssl/live/${NGINX_HOST}/privkey.pem
