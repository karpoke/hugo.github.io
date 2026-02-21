---
title: "Recuperar un disco corrupto"
date: 2018-01-30T20:36:00+01:00
draft: false
categories: ["admin"]
tags: ["copia de seguridad", "recuperación de datos", "dd", "pv", "ddrescue", "gddrescue"]
slug: "recuperar-un-disco-corrupto"
---
Un par de comandos útiles para recuperar datos de un disco problemático.

Para copiar el disco, mostrando una barra de progeso:

```
dd if=/dev/sda | pv | dd of=/dev/sdb conv=noerror,sync
```

Lanzamos `ddrescue`:
```
ddrescue -d -r3 /dev/sda /dev/sdb output.log
```
