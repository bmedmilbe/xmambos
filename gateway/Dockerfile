FROM nginx:alpine

RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*
ENV PORT=80
COPY local.conf /etc/nginx/nginx.conf.template

# 🚀 Comando atualizado para injetar a porta e as URLs dos microsserviços
CMD ["/bin/sh", "-c", "envsubst '\\$PORT \\$CMS_URL \\$TOUR_URL \\$REMITTANCE_URL \\$CERTIFICATE_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
