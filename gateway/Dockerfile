FROM nginx:alpine

RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*
ENV PORT=80
COPY local.conf /etc/nginx/nginx.conf.template

CMD ["/bin/sh", "-c", "envsubst '\\$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]