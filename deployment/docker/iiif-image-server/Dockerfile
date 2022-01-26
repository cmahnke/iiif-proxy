# syntax=docker/dockerfile:experimental

FROM adoptopenjdk/openjdk11:alpine

LABEL maintainer="cmahnke@gmail.com"

ENV REQ_BUILD="git maven gnutls-utils" \
    REQ_RUN="busybox libjpeg-turbo openjpeg tomcat-native" \
    BUILD_DIR="/tmp/build" \
    SERVER_DIR="/opt/iiif-server" \
    CONF_DIR=/etc/iiif-server \
    DATA_DIR="/data" \
    DOWNLOAD_CERTS="sammlungen.uni-goettingen.de images.sub.uni-goettingen.de manifests.sub.uni-goettingen.de"

RUN --mount=target=/mnt/build-context \
# Prepare to install dependencies
    apk --update upgrade && \
    apk add --no-cache $REQ_BUILD $REQ_RUN && \
    mkdir -p $BUILD_DIR $SERVER_DIR $CONF_DIR /var/log && \
# Copy entrypoint
    cp -r /mnt/build-context/deployment/docker/iiif-image-server/scripts/entrypoint.sh  / && \
# Get certificates, see https://serverfault.com/a/598759
    for SERVER in $DOWNLOAD_CERTS ; do \
        gnutls-cli --print-cert $SERVER </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $SERVER.crt ; \
        keytool -import -trustcacerts -keystore cacerts -storepass changeit -noprompt -alias $SERVER -file $SERVER.crt && \
        rm $SERVER.crt ; \
    done && \
# Include .dot files and directories in shell * - used for .git directories (doesn't work for Bourne Shell)
    cp -r /mnt/build-context/services/iiif-image-server/iiif-apis /mnt/build-context/services/iiif-image-server/iiif-server-hymir /mnt/build-context/services/iiif-image-server/hymir-quality-services $BUILD_DIR && \
    cd $BUILD_DIR/iiif-apis && \
    mvn -ntp clean install -Dfmt.skip -DskipTests -Dspotbugs.skip=true && \
    cd $BUILD_DIR/iiif-server-hymir && \
    mvn -ntp clean install -Dfmt.skip -DskipTests -Dmaven.gitcommitid.skip -Dspotbugs.skip=true && \
    rm ./target/*sources.jar ./target/*javadoc.jar && \
    mv ./target/*.jar $SERVER_DIR/ && \
    cd $BUILD_DIR/hymir-quality-services && \
    mvn -ntp clean install -Dfmt.skip -DskipTests && \
    rm ./target/original* ./target/*sources.jar && \
    mv ./target/*.jar $SERVER_DIR/ && \
    ln -s $SERVER_DIR/hymir-*-exec.jar $SERVER_DIR/hymir-exec.jar && \
    ln -s $SERVER_DIR/hymir-quality-services-*.jar $SERVER_DIR/hymir-quality-services.jar && \
    cd / && \

# Cleanup
    rm -rf $BUILD_DIR /root/.m2 /root/.groovy && \
    apk del ${REQ_BUILD}

WORKDIR $SERVER_DIR

VOLUME $DATA_DIR

ENTRYPOINT ["/entrypoint.sh"]
CMD [""]
