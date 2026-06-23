# gateway/Dockerfile
FROM nginx:alpine

# Instala ferramentas
RUN apk add --no-cache curl bind-tools

# Limpa configurações
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia configuração
COPY local.conf /etc/nginx/templates/local.conf.template

# Script inline no CMD
CMD echo "=== Gateway Starting ===" && \
    echo "CMS_URL: $CMS_URL" && \
    echo "TOUR_URL: $TOUR_URL" && \
    echo "REMITTANCE_URL: $REMITTANCE_URL" && \
    echo "CERTIFICATE_URL: $CERTIFICATE_URL" && \
    envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf && \
    echo "=== Nginx config generated ===" && \
    nginx -t && \
    nginx -g 'daemon off;'

EXPOSE 80