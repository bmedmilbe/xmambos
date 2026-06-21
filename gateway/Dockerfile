FROM nginx:1.25

RUN rm -f /etc/nginx/conf.d/default.conf

# Copy your configuration file as a template
COPY nginx.conf /etc/nginx/templates/default.conf.template
