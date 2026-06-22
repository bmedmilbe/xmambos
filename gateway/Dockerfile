FROM nginx:1.25

# 1. Clear out default configs
RUN rm -rf /etc/nginx/conf.d/*

# 2. Copy the config file into the native template processing directory
COPY nginx.conf /etc/nginx/templates/default.conf.template
