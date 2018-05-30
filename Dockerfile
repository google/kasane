FROM alpine:latest

ADD . /usr/src/kasane

RUN set -ex; \
    apk add --no-cache --no-progress bash git curl python3 libstdc++; \
    apk add --no-cache --no-progress --virtual .build-deps build-base python3-dev; \
    pip3 install -e /usr/src/kasane; \
    apk --no-progress del .build-deps; \
    curl -L https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl > /usr/bin/kubectl; \
    chmod +x /usr/bin/kubectl;

WORKDIR /app

CMD ["kasane", "show"]
