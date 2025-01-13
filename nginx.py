<VirtualHost *:80>
    ServerName your-domain.com  # Replace with your domain or server IP

    ProxyRequests Off
    ProxyPreserveHost On
    AllowEncodedSlashes NoDecode

    <Proxy http://127.0.0.1:8080/*>
        Order deny,allow
        Allow from all
    </Proxy>

    ProxyPass / http://127.0.0.1:8080/
    ProxyPassReverse / http://127.0.0.1:8080/
</VirtualHost>