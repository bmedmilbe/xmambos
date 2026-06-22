FROM nginx:1.25

# 1. Clear out all default settings and templates
RUN rm -rf /etc/nginx/conf.d/*
RUN rm -rf /etc/nginx/templates/*

# 2. Copy the file directly over the primary execution target
COPY nginx.conf /etc/nginx/conf.d/default.conf
