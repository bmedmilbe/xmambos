FROM nginx:1.25

# Instala o envsubst (caso não venha por padrão em algumas variantes)
RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

# Limpa configurações padrões
RUN rm -rf /etc/nginx/conf.d/*

# Garante um valor padrão caso a Railway demore a injetar o PORT
ENV PORT=80

# Copia o seu arquivo de configuração diretamente para a raiz do container como um template
COPY nginx.conf /etc/nginx/nginx.conf.template

# O PULO DO GATO: Executa o envsubst manualmente passando exatamente quais variáveis mudar, 
# gerando o arquivo final na pasta conf.d e iniciando o Nginx logo em seguida.
CMD /bin/sh -c "envsubst '\$PORT \$CMS_URL \$TOUR_URL \$REMITTANCE_URL \$CERTIFICATE_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
