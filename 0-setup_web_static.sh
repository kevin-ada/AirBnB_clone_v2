#!/usr/bin/env bash
# Update package information and install Nginx
apt-get -y update
apt-get -y install nginx

# Add the rewrite rule for /redirect_me to redirect to github.com/benkivuva
sed -i "/listen \[::\]:80 default_server/ a\\\trewrite ^/redirect_me http://github.com/benkivuva permanent;" /etc/nginx/sites-available/default

# Add a custom response header
sed -i "/listen \[::\]:80 default_server/ a\\\tadd_header X-Served-By \"\$HOSTNAME\";" /etc/nginx/sites-available/default

# Add the error_page directive for custom 404 page
sed -i "/redirect_me/ a\\\terror_page 404 /custom_404.html;" /etc/nginx/sites-available/default

# Start the Nginx service
service nginx start

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create an HTML file with content "Hello Nginx"
echo "Hello Nginx!" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Add the alias directive for serving web_static content and disable directory listing
sed -i "/^\tlocation \/ {$/ i\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n}" /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart

# Exit with success status
exit 0
