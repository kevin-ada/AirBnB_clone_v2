# Install Nginx and configure it
exec { 'update_apt':
  command => '/usr/bin/env apt-get -y update',
}

exec { 'install_nginx':
  command => '/usr/bin/env apt-get -y install nginx',
}

# Configure Nginx to serve web content
file { '/etc/nginx/sites-available/default':
  content => template('nginx/default.erb'),
  require => Exec['install_nginx'],
}

# Ensure Nginx is running and set to start on boot
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => [Exec['install_nginx'], File['/etc/nginx/sites-available/default']],
}

# Create directory structure for web_static
file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create a custom 404 error page
file { '/var/www/html/custom_404.html':
  ensure  => 'file',
  content => 'Ceci n\'est pas une page',
}

# Create a sample index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Hello nginx!',
}

# Create a symbolic link for web_static
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  require => [File['/data/web_static/releases/test/index.html']],
}

# Additional Nginx configuration, e.g., custom headers
file { '/etc/nginx/sites-available/default':
  content => template('nginx/default.erb'),
  require => File['/var/www/html/custom_404.html'],
}
