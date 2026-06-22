FROM nginx:1.25

# 1. Force clear out all default configuration files and template caches
RUN rm -rf /etc/nginx/conf.d/*
RUN rm -rf /etc/nginx/templates/*

# 2. Copy the file directly over the primary execution target folder
COPY nginx.conf /etc/nginx/conf.d/default.conf
