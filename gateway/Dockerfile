FROM nginx:alpine

RUN apk add --no-cache curl

COPY local.conf /etc/nginx/templates/local.conf.template

CMD envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'