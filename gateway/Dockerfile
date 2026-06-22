FROM nginx:alpine

# 1. Limpa todas as configurações padrões para evitar conflitos de portas
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# 2. Garante uma porta padrão caso a Railway demore a injetar a variável PORT no boot
ENV PORT=80

# 3. Define onde o arquivo convertido final será salvo pelo script nativo do Nginx
ENV NGINX_ENVSUBST_OUTPUT_DIR=/etc/nginx/conf.d

# 4. FILTRO ESSENCIAL: Protege as variáveis locais ($tenant, $host, $scheme) do Nginx. 
# Apenas as variáveis listadas aqui serão substituídas pelo envsubst.
ENV NGINX_ENVSUBST_FILTER='$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL'

# 5. Copia o seu arquivo de configuração local para a pasta de processamento de templates
COPY local.conf /etc/nginx/templates/default.conf.template

# O ponto de entrada padrão da imagem Alpine cuidará de rodar o envsubst e iniciar o Nginx
