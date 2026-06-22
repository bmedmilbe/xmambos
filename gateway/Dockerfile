FROM nginx:1.25

# Limpa configurações padrões
RUN rm -rf /etc/nginx/conf.d/*

# CORREÇÃO DE SEGURANÇA: Se a Railway não enviar o PORT, o Nginx assume 80 por padrão
ENV PORT=80

# Define onde o arquivo gerado deve ser salvo
ENV NGINX_ENVSUBST_OUTPUT_DIR=/etc/nginx/conf.d

# Diz ao Nginx para substituir APENAS as suas variáveis de ambiente
ENV NGINX_ENVSUBST_FILTER='$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL'

# Copia o seu arquivo local para a pasta de templates oficiais
COPY nginx.conf /etc/nginx/templates/default.conf.template
