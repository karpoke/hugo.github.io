---
title: "Solucionado el error «error: error running non-shared postrotate script for /var/log/samba/log.nmbd of '/var/log/samba/log.nmbd '»"
date: 2013-03-22T21:31:00+01:00
draft: false
categories: ["admin"]
tags: ["12.04", "error", "logrotate", "nmbd", "quantal", "quetzal", "samba", "smbd", "ubuntu"]
slug: "solucionado-el-error-error-error-running-non-shared-postrotate-script-for-varlogsambalog-nmbd-of-varlogsambalog-nmbd"
---
Si nos encontramos con el siguiente error:

```
error: error running non-shared postrotate script for /var/log/samba/log.nmbd of '/var/log/samba/log.nmbd '
```

En Ubuntu 12.04.2, con la versión de `samba` 3.6.3, podría producirse
cuando el [_script_ de `logrotate` para `samba`][script de logrotate para samba]
intenta hacer un `reload` del servicio `nmbd` y éste no está en ejecución.
Necesita un pequeño cambio en los comandos utilizados en la directiva `postrotate`:
deberemos cambiar `reload` por `reload --quiet`, quedando finalmente así
las respectivas líneas en el fichero `/etc/logrorate.d/samba`:

```
reload --quiet smbd 2>/dev/null
reload --quiet nmbd 2>/dev/null
```

  [script de logrotate para samba]: http://dev-eole.ac-dijon.fr/issues/4524
