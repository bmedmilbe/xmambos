FROM nginx:alpine

ARG CACHE_BYPASS=1 

# 1. Limpa todas as configurações padrão para evitar conflitos
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# 2. Copia o local.conf para a raiz do nginx com outro nome (evita o script automático da imagem)
COPY local.conf /etc/nginx/local.conf.template

ENV PORT=80

# 3. 🚀 Força o envsubst a ler APENAS a variável $PORT e $CMS_URL, ignorando o resto para não quebrar as outras URLs
CMD ["/bin/sh", "-c", "envsubst '\\$PORT \\$CMS_URL' < /etc/nginx/local.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]

EXPOSE 80