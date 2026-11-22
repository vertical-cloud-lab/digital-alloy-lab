# CAMotics 1.2.0 (the last release, 2019) on Ubuntu 18.04, the newest Ubuntu that still ships the
# libraries its binaries link against: libv8.so.3.14.5 (V8 3.14) and libssl.so.1.1 / libcrypto.so.1.1.
# The .deb does not declare libQt5WebSockets.so.5, so libqt5websockets5 is added by hand.
FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl xvfb xauth \
 && curl -fsSL -o /tmp/camotics.deb \
      https://github.com/CauldronDevelopmentLLC/CAMotics/releases/download/1.2.0-release/camotics_1.2.0_amd64.deb \
 && echo "5dc5ba0c53a8eb8ce6b3bd2c3bd903465fde860742a7764f2511b188a507c2c0  /tmp/camotics.deb" | sha256sum -c - \
 && apt-get install -y --no-install-recommends /tmp/camotics.deb libqt5websockets5 \
 && rm /tmp/camotics.deb && rm -rf /var/lib/apt/lists/*
WORKDIR /work
