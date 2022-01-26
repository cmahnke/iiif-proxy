# syntax=docker/dockerfile:experimental

ARG WEB_ROOT=/var/www/html
ARG DEBUG=false

FROM node:17-alpine AS builder

LABEL maintainer="cmahnke@gmail.com"

ARG WEB_ROOT
ARG DEBUG

RUN --mount=target=/mnt/build-context \
    mkdir -p $WEB_ROOT && \
    cp -r /mnt/build-context/services/web/viewer $WEB_ROOT/ && \
    cd $WEB_ROOT/viewer && \
    sed -i -E 's/([A-Z_-]*)=/\1=/g' .env && \
    if [ -z "$DEBUG" ] || [ "$DEBUG" != "true" ] ; then echo "Emptying dev .env" ; sed -i -E 's/([A-Z_-]*)=.*/\1=/g' .env ; fi && \
    npm install && \
    npm run build


FROM nginx:stable-alpine

ARG WEB_ROOT

ENV NGINX_CACHE_DIR=/data/nginx/cache \
    REQ_BUILD="gnutls-utils" \
    DOWNLOAD_CERTS="sammlungen.uni-goettingen.de images.sub.uni-goettingen.de manifests.sub.uni-goettingen.de"
    #REQ_BUILD="certbot certbot-nginx"

RUN --mount=target=/mnt/build-context \
    apk --update upgrade && \
    apk add --no-cache $REQ_BUILD $REQ_BUILD && \
    mkdir -p $WEB_ROOT/viewer $NGINX_CACHE_DIR /etc/letsencrypt /var/www/certbot /etc/nginx/ssl/backends /etc/nginx/ssl/live/localhost && \
    # Get certificates, see https://serverfault.com/a/598759
    for SERVER in $DOWNLOAD_CERTS ; do \
        gnutls-cli --print-cert $SERVER </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $SERVER.crt ; \
        mv $SERVER.crt /etc/nginx/ssl/backends/ ; \
    done && \
    # Generate dummy certificates
    printf 'organization = "Forum Wissen"\nstate = "Lower Saxony"\ncountry = DE\n' > ssl.template && \
    certtool --generate-privkey --sec-param High --outfile /etc/nginx/ssl/live/localhost/privkey.pem && \
    certtool --generate-self-signed --load-privkey /etc/nginx/ssl/live/localhost/privkey.pem --template /ssl.template > /etc/nginx/ssl/live/localhost/fullchain.pem && \
    rm -f /ssl.template && \
    # Copy additional entrypoint scrips
    if [ -z "$(ls -A /mnt/build-context/deployment/docker/web/entrypoint.d/)" ]; then \
        echo "No additional entrypoint scripts found!" ; \
    else \
        echo "Copying $(ls -A /mnt/build-context/deployment/docker/web/entrypoint.d/)" && \
        cp /mnt/build-context/deployment/docker/web/entrypoint.d/* /docker-entrypoint.d/ ; fi && \
    curl -o $WEB_ROOT/favicon.ico https://iiif.io/api/assets/favicon.ico && \
    apk del $REQ_BUILD $REQ_BUILD && \
    rm -rf /var/cache/apk/*

COPY --from=builder $WEB_ROOT/viewer/dist/* $WEB_ROOT/viewer/
