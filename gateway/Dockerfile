FROM nginx:1.25

# 1. Clear out all native settings
RUN rm -rf /etc/nginx/conf.d/*

# 2. Copy the file into the template directory using a template file signature
# The official Nginx image reads this folder on boot, replaces all ${VARIABLES}, 
# and automatically outputs the clean file straight into /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/templates/default.conf.template
