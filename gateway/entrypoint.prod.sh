#!/bin/sh

echo "=== Gateway Starting ==="
echo "PORT: $PORT"
echo "CMS_URL: ${CMS_URL:-NOT SET}"
echo "TOUR_URL: ${TOUR_URL:-NOT SET}"
echo "REMITTANCE_URL: ${REMITTANCE_URL:-NOT SET}"
echo "CERTIFICATE_URL: ${CERTIFICATE_URL:-NOT SET}"
echo ""

echo "=== Testing service discovery ==="
for service in cms tour remittance certificate; do
    if nslookup $service.railway.internal > /dev/null 2>&1; then
        echo "✅ $service.railway.internal resolves"
    else
        echo "❌ $service.railway.internal does not resolve"
        # Se não resolver, verifica se é o certificate (pode não existir)
        if [ "$service" = "certificate" ]; then
            echo "⚠️  Certificate service not found, will skip"
            export CERTIFICATE_URL=""
        fi
    fi
done

echo ""
echo "=== Final URLs ==="
echo "CMS_URL: ${CMS_URL:-EMPTY}"
echo "TOUR_URL: ${TOUR_URL:-EMPTY}"
echo "REMITTANCE_URL: ${REMITTANCE_URL:-EMPTY}"
echo "CERTIFICATE_URL: ${CERTIFICATE_URL:-EMPTY}"
echo ""

echo "=== Generating Nginx config ==="
envsubst '$PORT $CMS_URL $TOUR_URL $REMITTANCE_URL $CERTIFICATE_URL' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf

echo "=== Testing Nginx config ==="
nginx -t

echo ""
echo "=== Starting Nginx ==="
exec nginx -g 'daemon off;'