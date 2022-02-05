#!/bin/sh

mkdir -p /etc/nginx/ssl/live/${NGINX_HOST}

if [ -n  "${NGINX_HOST}" ] ; then
    if ! [ /etc/nginx/ssl/live/localhost/fullchain.pem -ef "/etc/nginx/ssl/live/${NGINX_HOST}/fullchain.pem" ] ;  then
        cp -u /etc/nginx/ssl/live/localhost/fullchain.pem /etc/nginx/ssl/live/${NGINX_HOST}/fullchain.pem
    fi

    if ! [ /etc/nginx/ssl/live/localhost/privkey.pem -ef "/etc/nginx/ssl/live/${NGINX_HOST}/privkey.pem" ] ;  then
        cp -u /etc/nginx/ssl/live/localhost/privkey.pem /etc/nginx/ssl/live/${NGINX_HOST}/privkey.pem
    fi
fi
