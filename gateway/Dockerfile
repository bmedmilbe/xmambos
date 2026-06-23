# gateway/Dockerfile
FROM nginx:alpine

# Copia a configuração diretamente
COPY local.conf /etc/nginx/conf.d/default.conf

# Comando simples para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80