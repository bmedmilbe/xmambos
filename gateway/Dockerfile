FROM nginx:alpine

ARG CACHE_BYPASS=1 

# Instala ferramentas
RUN apk add --no-cache curl bind-tools

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia configuração
COPY local.conf /etc/nginx/templates/local.conf.template
COPY entrypoint.prod.sh /entrypoint.prod.sh

# Torna o script executável
RUN chmod +x /entrypoint.prod.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.prod.sh"]