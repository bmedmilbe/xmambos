# No seu projeto local (fora do container)
cat > docker-entrypoint.sh << 'EOF'
#!/bin/sh

echo "=== Gateway Starting ==="

# Função para resolver IP
resolve_ip() {
    local service=$1
    local ip=$(nslookup $service.railway.internal 2>/dev/null | grep "Address" | tail -1 | awk '{print $2}')
    if [ -z "$ip" ]; then
        echo "$service.railway.internal"
    else
        echo "$ip"
    fi
}

CMS_IP=$(resolve_ip cms)
TOUR_IP=$(resolve_ip tour)
REMITTANCE_IP=$(resolve_ip remittance)
CERTIFICATE_IP=$(resolve_ip certificate)

echo "CMS: $CMS_IP"
echo "TOUR: $TOUR_IP"
echo "REMITTANCE: $REMITTANCE_IP"
echo "CERTIFICATE: $CERTIFICATE_IP"

# Gera configuração
envsubst '$PORT $CMS_IP $TOUR_IP $REMITTANCE_IP $CERTIFICATE_IP' < /etc/nginx/templates/local.conf.template > /etc/nginx/conf.d/default.conf

echo "=== Nginx config generated ==="
nginx -t

exec nginx -g 'daemon off;'
EOF

# Torna o script executável
chmod +x docker-entrypoint.sh