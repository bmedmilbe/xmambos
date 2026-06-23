FROM nginx:alpine

RUN apk add --no-cache curl

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia a configuração como template
COPY local.conf /etc/nginx/templates/local.conf.template

# Gera a configuração final com envsubst
CMD envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'

EXPOSE 80