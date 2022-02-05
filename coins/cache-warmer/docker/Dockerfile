# syntax=docker/dockerfile:experimental

FROM php:7.4-cli-alpine

LABEL maintainer="cmahnke@gmail.com"

ENV REQ_BUILD="openjdk11-jre curl sed" \
    REQ_RUN="busybox" \
    SAXON_URL="https://repo1.maven.org/maven2/net/sf/saxon/Saxon-HE/11.1/Saxon-HE-11.1.jar" \
    RESOLVER_URL="https://repo1.maven.org/maven2/org/xmlresolver/xmlresolver/4.1.2/xmlresolver-4.1.2.jar" \
    BUILD_DIR="/tmp/build" \
    DATA_DIR="/data" \
    FILE_LIST=/data/identifiers.lst

RUN --mount=target=/mnt/build-context \
# Prepare to install dependencies
    apk --update upgrade && \
    apk add --no-cache $REQ_BUILD $REQ_RUN && \
    mkdir -p $BUILD_DIR /opt/saxon $DATA_DIR $DATA_DIR/lido/ && \
    ln -s $DATA_DIR/ $BUILD_DIR$DATA_DIR && \
    cd $BUILD_DIR && \
# Get Saxon
    curl $SAXON_URL --output /opt/saxon/Saxon-HE-11.1.jar && \
    curl $RESOLVER_URL --output /opt/saxon/xmlresolver-4.1.2.jar  && \
    ln -s /opt/saxon/Saxon-HE-11.1.jar /opt/saxon/saxon.jar && \
    ln -s /opt/saxon/xmlresolver-4.1.2.jar /opt/saxon/xmlresolver.jar && \
# Get Composer
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php -r "if (hash_file('sha384', 'composer-setup.php') === '906a84df04cea2aa72f40b5f787e49f22d4c2f19492ac310e8cba5b96ac8b64115ac402c8cd292b8a03482574915d1a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
    php composer-setup.php && \
    php -r "unlink('composer-setup.php');" && \
    mv composer.phar /usr/local/bin/composer && \
# Copy files
    cp -r /mnt/build-context/coins/cache-warmer/* . && \
    cd harvester && \
    COMPOSER_ALLOW_SUPERUSER=1 php /usr/local/bin/composer install && \
# Start harvester
    php src/harvester.php && \
    mv $BUILD_DIR$DATA_DIR/*.xml $DATA_DIR/lido/ && \
    cd .. && \
# Start converter
    java -Xmx2048m -cp /opt/saxon/saxon.jar:/opt/saxon/xmlresolver.jar net.sf.saxon.Transform -xsl:"$BUILD_DIR/xslt/extract-image-identifiers.xsl" -s:"$BUILD_DIR/xslt/empty.xml" collection=$DATA_DIR/lido/ > $FILE_LIST && \
# Copy entrypoint
    cp docker/entrypoint.d/entrypoint.sh / && \
# Cleanup
    rm -rf /usr/local/bin/composer $BUILD_DIR /root/.composer && \
    apk del ${REQ_BUILD}

VOLUME $DATA_DIR
