FROM nginx:1.25

# Clear out any native configuration fragments
RUN rm -rf /etc/nginx/conf.d/*

# Place the file into the template engine structure
COPY nginx.conf /etc/nginx/templates/default.conf.template
