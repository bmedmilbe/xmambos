FROM nginx:alpine

ARG CACHE_BYPASS=1 

# 1. Limpa todas as configurações padrão para evitar conflitos
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# 2. Copia o local.conf para a raiz do nginx como template
COPY local.conf /etc/nginx/local.conf.template

# 🎯 REMOVIDO: ENV PORT=80 (Deixamos o Railway injetar a porta real do ambiente)

# 3. Executa o envsubst aplicando as variáveis de ambiente reais
CMD ["/bin/sh", "-c", "envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/local.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]

EXPOSE 80