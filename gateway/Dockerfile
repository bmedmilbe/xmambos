FROM nginx:alpine

ARG CACHE_BYPASS=1 

# Instala ferramentas de debug (opcional)
RUN apk add --no-cache curl

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia a configuração
COPY local.conf /etc/nginx/templates/local.conf.template

# Script de inicialização
CMD envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'

EXPOSE 80