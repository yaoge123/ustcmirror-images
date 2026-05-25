FROM ustcmirror/base:alpine-edge
LABEL maintainer="Jian Zeng <anonymousknight96 AT gmail.com>"
RUN apk add --no-cache git && \
    git config set --global pack.windowMemory 100m && \
    git config set --global pack.threads 2 && \
    git config set --global maintenance.auto false
ADD sync.sh /
