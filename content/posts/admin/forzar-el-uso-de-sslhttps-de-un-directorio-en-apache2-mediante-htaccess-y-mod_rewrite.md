---
title: "Forzar el uso de SSL/HTTPS de un directorio en Apache2 mediante .htaccess y mod_rewrite"
date: 2012-05-10T15:35:00+01:00
categories: ["admin"]
tags: [".htaccess", "https", "mod_rewrite", "ssl"]
slug: "forzar-el-uso-de-sslhttps-de-un-directorio-en-apache2-mediante-htaccess-y-mod_rewrite"
---
Si queremos que el acceso a un directorio concreto, es decir, que afecte
únicamente la ruta relativa en la URL que accede a ese directorio, se
realice mediante una conexión segura, suponiendo que ya tenemos
configurado el servidor de forma adecuada, basta incluir en ese
directorio un fichero `.htaccess` que contenga:

```
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
```

Así, si por ejemplo, queremos que la ruta `http://localhost/secure/` se
acceda de forma segura, suponiendo que el `DocumentRoot` apunta a
`/var/www`:

```
$ pwd
/var/www/secure
```

```
$ cat .htaccess
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
```
