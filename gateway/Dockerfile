FROM nginx:alpine

# Limpa todas as configurações padrão
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# 💡 VALORES PADRÃO (Fallbacks): Se as variáveis não existirem no painel do Railway,
# estes valores evitam que o Nginx quebre na inicialização.
ENV PORT=80
ENV CMS_URL=cms.railway.internal
ENV TOUR_URL=tour.railway.internal
ENV REMITTANCE_URL=remittance.railway.internal
ENV CERTIFICATE_URL=certificate.railway.internal

# Copia o seu ficheiro local.conf para a raiz
COPY local.conf /etc/nginx/nginx.conf.template

# 🚀 Executa o envsubst completo em todas as variáveis do arquivo
CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]

EXPOSE 80