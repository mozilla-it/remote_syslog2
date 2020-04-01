ARG ALPINE_VERSION=3.11.5
ARG REMOTE_SYSLOG2_VERSION=v0.20

FROM alpine:${ALPINE_VERSION} AS builder
LABEL stage=intermediate

# required after the FROM statement to pass through
ARG REMOTE_SYSLOG2_VERSION

RUN apk --no-cache add -t deps wget ca-certificates \
  && wget -q -O - https://github.com/papertrail/remote_syslog2/releases/download/${REMOTE_SYSLOG2_VERSION}/remote_syslog_linux_amd64.tar.gz \
  | tar -zxf - \
  && apk del deps

FROM alpine:${ALPINE_VERSION}
COPY --from=builder remote_syslog remote_syslog

ENTRYPOINT ["/remote_syslog/remote_syslog", "-D"]
