FROM nginx:1.25

# Clear out any default configuration files
RUN rm -rf /etc/nginx/conf.d/*
RUN rm -rf /etc/nginx/templates/*

# Copy your configuration file directly over the primary execution target
COPY nginx.conf /etc/nginx/conf.d/default.conf
