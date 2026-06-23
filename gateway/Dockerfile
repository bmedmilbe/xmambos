FROM nginx:alpine

# Limpa configurações padrão
RUN rm -rf /etc/nginx/conf.d/*

# Copia a configuração
COPY local.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]