FROM nginx:alpine

# 1. Limpa todas as configurações padrões
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# 2. Garante uma porta padrão caso a Railway demore a injetar a variável PORT
ENV PORT=80

# 3. Copia o arquivo diretamente como um template bruto
COPY local.conf /etc/nginx/nginx.conf.template

# 4. CORREÇÃO: Passando as variáveis com escape para o envsubst não apagar as variáveis do Nginx
CMD ["/bin/sh", "-c", "envsubst '\\$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]