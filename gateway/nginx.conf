FROM nginx:1.25

# Instala ferramentas básicas
RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

# Limpa configurações padrões
RUN rm -rf /etc/nginx/conf.d/*

# Copia o template de configuração
COPY nginx.conf /etc/nginx/nginx.conf.template

# Se a variável PORT estiver vazia, o script abaixo força o valor 80 antes de gerar o arquivo do Nginx
CMD /bin/sh -c "if [ -z \"\$PORT\" ]; then export PORT=80; fi && envsubst '\$PORT \$CMS_URL \$TOUR_URL \$REMITTANCE_URL \$CERTIFICATE_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
