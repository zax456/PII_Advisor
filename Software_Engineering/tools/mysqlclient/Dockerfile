FROM alpine:latest
RUN apk update --no-cache
RUN apk upgrade --no-cache
RUN apk add --no-cache mysql-client
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint
ENTRYPOINT [ "/bin/entrypoint" ]
