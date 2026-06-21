FROM nginx:1.25

# Clear out all native settings
RUN rm -rf /etc/nginx/conf.d/*

# Copy the file directly over the fallback location
COPY nginx.conf /etc/nginx/conf.d/default.conf
