FROM nginx:alpine

ARG CACHE_BYPASS=1 

# Instala ferramentas
RUN apk add --no-cache curl bind-tools

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia configuração
COPY local.conf /etc/nginx/templates/local.conf.template

# Script de inicialização com validação de serviços
CMD echo "=== Gateway Starting ===" && \
    echo "PORT: $PORT" && \
    echo "CMS_URL: ${CMS_URL:-NOT SET}" && \
    echo "TOUR_URL: ${TOUR_URL:-NOT SET}" && \
    echo "REMITTANCE_URL: ${REMITTANCE_URL:-NOT SET}" && \
    echo "CERTIFICATE_URL: ${CERTIFICATE_URL:-NOT SET}" && \
    echo "" && \
    echo "=== Testing service discovery ===" && \
    for service in cms tour remittance certificate certificates; do \
        echo "Checking $service.railway.internal..."; \
        if nslookup $service.railway.internal > /dev/null 2>&1; then \
            echo "✅ $service.railway.internal resolves"; \
            # Se a variável não estiver definida, define com porta 8000
            var_name=$(echo $service | tr '[:lower:]' '[:upper:]')_URL; \
            if [ -z "${!var_name}" ]; then \
                echo "⚠️  $var_name not set, using default: $service.railway.internal:8000"; \
                export $var_name="$service.railway.internal:8000"; \
            fi \
        else \
            echo "❌ $service.railway.internal does not resolve"; \
        fi; \
    done && \
    echo "" && \
    echo "=== Final URLs ===" && \
    echo "CMS_URL: $CMS_URL" && \
    echo "TOUR_URL: $TOUR_URL" && \
    echo "REMITTANCE_URL: $REMITTANCE_URL" && \
    echo "CERTIFICATE_URL: $CERTIFICATE_URL" && \
    echo "" && \
    envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf && \
    echo "=== Generated config (first 50 lines) ===" && \
    head -50 /etc/nginx/conf.d/default.conf && \
    echo "" && \
    echo "=== Testing Nginx config ===" && \
    nginx -t && \
    echo "" && \
    echo "=== Starting Nginx ===" && \
    nginx -g 'daemon off;'

EXPOSE 80