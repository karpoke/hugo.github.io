---
title: "Obtener el listado de rangos de IPs asociados a un dominio"
date: 2014-06-01T12:57:00+01:00
categories: ["admin"]
tags: ["dig", "host", "OriginAS", "whois"]
slug: "obtener-el-listado-de-rangos-de-ips-asociados-a-un-dominio"
---
Si queremos obtener el listado de rangos de IPs que puedan estar
asociadas a un dominio, por ejemplo para bloquearlo, podemos ejecutar:

```
$ IP=$(dig +short www.example.com | grep -Eo '([0-9]{1,3}\.?){4}' | head -1)
$ AS=$(whois $IP | awk '/OriginAS/{print $2}')
$ test -n "$AS" && whois -h whois.radb.net '!g'$AS | tr -d "\n" | tr " " "\n" | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4
```

En la primera línea, obtenemos la IP asociada al dominio. En la segunda,
obtenemos el registro _origin_, el cual utilizamos en la tercera línea
para consultar a whois.radb.net el rango de IPs y mostrar las IPs una
por línea.

Esto nos da el listado de IPs v4, si queremos las IPs v6, podemos
modificar ligeramente la tercera línea:

```
$ whois -h whois.radb.net -- "-i origin $AS" | awk '/^route6:/{print $2}'
```

Referencias
-----------

» [How can I list all IPs relating to a single AS?][]

  [How can I list all IPs relating to a single AS?]: http://www.fir3net.com/How-Tos/how-can-i-list-all-ips-relating-to-a-single-as.html
