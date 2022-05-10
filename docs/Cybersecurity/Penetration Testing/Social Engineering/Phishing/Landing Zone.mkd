### Configuring TLS certificates for a web server

```bash
sudo apt install nginx python3 python3-pip certbot python3-certbot-nginx -y
sudo certbot --domain "$DOMAIN_NAME" -m "$VERIFICATION_EMAIL" --non-interactive --nginx --agree-tos
```

### Nginx rewriting rules

Redirect all requests to the landing page:

```bash
cat /etc/nginx/sites-available/default

server {
        rewrite ^(.*) /index.html;
}
```

### Nginx redirect proxy

Redirect all requests to another server:

- https://blog.logrocket.com/how-to-run-a-node-js-server-with-nginx/

```json
server{
    listen 80;
    server_name wach.quest;
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # location /overview {
        #     proxy_pass http://127.0.0.1:3000$request_uri;
        #     proxy_redirect off;
        # }
    }
}
```
