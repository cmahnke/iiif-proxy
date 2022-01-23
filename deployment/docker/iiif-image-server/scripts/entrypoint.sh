#!/bin/sh

IMAGE_QUALITY_LIB=$SERVER_DIR/hymir-quality-services.jar
HYMIR_JAR=$SERVER_DIR/hymir-exec.jar

if [[ -n "$HYMIR_RULES" && -r "$HYMIR_RULES" ]] ; then
    HYMIR_OPTS="$HYMIR_OPTS --spring.config.additional-location=$HYMIR_RULES"
fi

if [ -n "$HYMIR_PORT" ] ; then
    HYMIR_OPTS="$HYMIR_OPTS --server.port=$HYMIR_PORT"
else
    HYMIR_OPTS="$HYMIR_OPTS --server.port=8080"
fi

if [ -n "$SPRING_PROFILE" ] ; then
    HYMIR_OPTS="$HYMIR_OPTS --spring.profiles.active=$SPRING_PROFILE"
fi

if [[ -n "$HYMIR_LOG_CONFIG" && -r "$HYMIR_LOG_CONFIG" ]] ; then
    HYMIR_OPTS="$HYMIR_OPTS --logging.config=file:$HYMIR_LOG_CONFIG -DLogback.configurationFile=$HYMIR_LOG_CONFIG "
fi

HYMIR_CP="$IMAGE_QUALITY_LIB"

echo "Starting with '$HYMIR_OPTS', class path '$HYMIR_CP'"

# Main Class de.digitalcollections.iiif.hymir.Application
#exec java -cp $HYMIR_CP org.springframework.boot.loader.JarLauncher  $HYMIR_OPTS "$@"

exec java -cp $HYMIR_JAR -Dloader.path=$HYMIR_CP org.springframework.boot.loader.PropertiesLauncher $HYMIR_OPTS "$@"
