#!/bin/bash
set -e

# === Variables ===
REPO_URL="git@github.com:yourusername/scoutos.git"
APP_DIR="/var/www/scoutos"
BRANCH="main"
DOMAIN="yourdomain.com"
EMAIL="youremail@example.com" # for SSL cert registration
DOCKER_COMPOSE_VERSION="2.16.0"

echo "Starting ScoutOS full server setup..."

# 1. Update & install essentials
echo "Updating packages..."
sudo apt update && sudo apt upgrade -y
echo "Installing prerequisites..."
sudo apt install -y git curl apt-transport-https ca-certificates software-properties-common nginx python3-certbot-nginx ufw

# 2. Install Docker if missing
if ! command -v docker &> /dev/null; then
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  rm get-docker.sh
  sudo usermod -aG docker $USER
fi

# 3. Install Docker Compose if missing or outdated
if ! command -v docker-compose &> /dev/null || [[ $(docker-compose --version) != *"$DOCKER_COMPOSE_VERSION"* ]]; then
  echo "Installing Docker Compose..."
  sudo curl -L "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

# 4. Clone or update ScoutOS repo
if [ ! -d "$APP_DIR" ]; then
  echo "Cloning ScoutOS repository..."
  git clone $REPO_URL $APP_DIR
else
  echo "Updating ScoutOS repository..."
  cd $APP_DIR
  git fetch origin
  git reset --hard origin/$BRANCH
fi

cd $APP_DIR

# 5. Build and run containers
echo "Building and starting Docker containers..."
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d

# 6. Configure Nginx for ScoutOS
NGINX_CONF="/etc/nginx/sites-available/scoutos"
sudo tee $NGINX_CONF > /dev/null << EOF_NGINX
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /ws/ {
        proxy_pass http://localhost:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }

    location / {
        root $APP_DIR/frontend/build;
        index index.html;
        try_files \$uri /index.html;
    }
}
EOF_NGINX

sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 7. Obtain SSL cert with Certbot
if ! command -v certbot &> /dev/null; then
  echo "Installing Certbot..."
  sudo apt install -y certbot python3-certbot-nginx
fi

sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m $EMAIL

# 8. Configure UFW firewall
echo "Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

# 9. Install Prometheus Node Exporter for monitoring
if ! command -v node_exporter &> /dev/null; then
  echo "Installing Prometheus Node Exporter..."
  cd /tmp
  NODE_EXPORTER_VERSION="1.5.0"
  wget https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
  tar xzf node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
  sudo cp node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter /usr/local/bin/
  sudo useradd -rs /bin/false node_exporter

  sudo tee /etc/systemd/system/node_exporter.service > /dev/null << EOL
[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOL

  sudo systemctl daemon-reload
  sudo systemctl enable node_exporter
  sudo systemctl start node_exporter

  echo "Prometheus Node Exporter installed and running."
fi

echo "ScoutOS server setup completed successfully!"
echo "Please reboot or log out/in for docker group permissions to apply."
