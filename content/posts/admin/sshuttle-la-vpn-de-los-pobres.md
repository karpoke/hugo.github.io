---
title: "sshuttle, la VPN de los pobres"
date: 2013-10-20T21:03:00+01:00
categories: ["admin"]
tags: ["dns", "proxy", "ssh", "sshuttle", "tunnel", "vpn"]
slug: "sshuttle-la-vpn-de-los-pobres"
---
[shuttle][] es una herramienta que nos permite redirigir todo el tráfico
a través de una conexión SSH, incluyendo las peticiones DNS. Está
disponible tanto en los repositorios como en GitHub.

Su uso es sencillo. Para establecer la conexión:

```
$ sshuttle --D --pidfile=/tmp/sshuttle.pid -r user@server:1234 --dns 0/0
```

Para terminarla:

```
$ kill $(cat /tmp/sshuttle.pid)
```

  [shuttle]: https://github.com/apenwarr/sshuttle
