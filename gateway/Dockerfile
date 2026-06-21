FROM nginx:1.25

# 1. Forcefully delete any native fallback configs that trigger the welcome page
RUN rm -f /etc/nginx/conf.d/default.conf

# 2. Overwrite the default config location directly with your custom multi-tenant router
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 3. Ensure proper file reading permissions inside the container layers
RUN chmod 644 /etc/nginx/conf.d/default.conf
