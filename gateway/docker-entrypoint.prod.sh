# gateway/Dockerfile
FROM nginx:alpine

# Instala ferramentas necessárias
RUN apk add --no-cache curl bind-tools

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# Copia o script de entrada
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Torna o script executável
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]