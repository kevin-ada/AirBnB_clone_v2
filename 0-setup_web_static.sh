#!/usr/bin/env bash

# Step 1: Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Step 2: Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Step 3: Create a fake HTML file for testing
echo "<html><head></head><body>Hello, Nginx!</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Step 4: Create or recreate symbolic link
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Step 5: Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Step 6: Update Nginx configuration with an alias
config_file="/etc/nginx/sites-available/default"
config_content="server {
    listen 80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html;
    }
    location / {
        add_header X-Served-By \$hostname;
        proxy_set_header Host \$host;
        proxy_pass http://127.0.0.1:5000;
    }
    location /redirect_me {
        rewrite ^/redirect_me http://www.github.com/benkivuva permanent;
    }
    error_page 404 /404.html;
    location /404 {
        internal;
    }
}"

# Backup the existing Nginx configuration
sudo cp "$config_file" "${config_file}.bak"

# Update Nginx configuration
echo "$config_content" | sudo tee "$config_file" > /dev/null

# Restart Nginx to apply changes
sudo service nginx restart

# Exit with success status
exit 0
