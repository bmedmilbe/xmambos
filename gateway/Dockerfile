FROM nginx:alpine

ARG CACHE_BYPASS=1 

# Instala ferramentas de debug (opcional)
RUN apk add --no-cache curl bind-tools

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia a configuração
COPY local.conf /etc/nginx/templates/local.conf.template

# Gera a configuração final com envsubst
CMD echo "=== Gateway Starting ===" && \
    echo "PORT: $PORT" && \
    echo "CMS_URL: ${CMS_URL:-NOT SET}" && \
    echo "TOUR_URL: ${TOUR_URL:-NOT SET}" && \
    echo "REMITTANCE_URL: ${REMITTANCE_URL:-NOT SET}" && \
    echo "CERTIFICATE_URL: ${CERTIFICATE_URL:-NOT SET}" && \
    echo "" && \
    echo "=== Generating Nginx config ===" && \
    envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf && \
    echo "=== Generated config (first 30 lines) ===" && \
    head -30 /etc/nginx/conf.d/default.conf && \
    echo "" && \
    echo "=== Nginx config test ===" && \
    nginx -t && \
    echo "" && \
    echo "=== Starting Nginx ===" && \
    nginx -g 'daemon off;'

EXPOSE 80