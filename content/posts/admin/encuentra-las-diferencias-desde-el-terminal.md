---
title: "Encuentra las diferencias... desde el terminal"
date: 2011-03-29T22:08:00+01:00
categories: ["admin"]
tags: ["compose difference", "composite", "convert", "crop", "imagemagick"]
slug: "encuentra-las-diferencias-desde-el-terminal"
---
Supongamos que queremos [encontrar las diferencias][] en la siguiente
imagen:

![diferencias]({static}/images/diferencias-300x233.png)

_Fuente: [taringa.net][]_

Tal como se muestra en la tira cómica, se puede hacer utilizando las
herramientas de la suite `imagemagick`, en particular, `composite`.

Primero, creamos una imagen con cada mitad de la imagen original:

```
$ convert diferencias.jpg -crop 50%x100% out.png
```

Esto crea dos ficheros, `out-0.png` y `out-0.png`, uno con la mitad
izquierda y otro con la mitad izquierda.

Vamos a obtener las diferencias:

```
$ composite out-0.png out-1.png -compose difference diferencias-out.png
```

![diferencias out]({static}/images/diferencias-out-193x300.png)

  [encontrar las diferencias]: http://www.linuxhispano.net/2011/03/29/diferencias/
  [taringa.net]: http://www.taringa.net/posts/imagenes/6577248/encuentra-las-diferencias.html
