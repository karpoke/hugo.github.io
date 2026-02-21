---
title: "Crear un repositorio de paquetes local"
date: 2014-11-12T18:57:00+01:00
draft: false
categories: ["admin"]
tags: ["apt", "apt-cdrom", "aptitude", "dpkg-dev", "dpkg-scanpackages", "sources.list"]
slug: "crear-un-repositorio-de-paquetes-local"
---
Al instalar algunos programas a partir del código fuente, tenemos la
opción de [crear paquetes `.deb` mediante `checkinstall`][crear paquetes .deb mediante checkinstall], de tal forma
que nos sea más sencillo reinstalarlos, o instalarlos en otros equipos.

La idea es crear un repositorio local que podamos acceder mediante
`apt-get` o `aptitude`, y así podemos delegar la instalación de
dependencias.


Directorio
----------

Si el número de paquetes es relativamente pequeño, de una misma
distribución, de una sola arquitectura, etc, lo único que necesitamos es
crear un listado de los paquetes disponibles y añadirlo como fuente en
el `sources.list`. Si no es el caso, ya sea porque tenemos paquetes para
diferentes distribuciones o diferentes arquitecturas, deberemos
organizar los paquetes siguiendo una jerarquía concreta.

Antes de continuar, instalaremos el paquete `apt-dev`, el cual contiene
las herramientas necesarias.

Supongamos que tenemos los paquetes en el directorio `/var/local/deb`.
Para crear el listado de paquetes ejecutamos:

```
$ cd /var/local/deb
$ sudo su
# dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
```

Deberemos ejecutar ese comando cada vez que añadamos o eliminemos un
nuevo paquete.

El siguiente paso es actualizar el fichero de fuentes
`/etc/apt/sources.list`, añadiendo la línea:

```
deb file:/var/local/deb ./
```

Una vez actualizada la lista de paquetes disponibles, ya podremos
instalarlos normalmente:

```
$ sudo aptitude update
```

CD ROM
------

Ya no es algo tan común, pero si necesitamos grabar los paquetes en un
CD, basta ejecutar el siguiente comando para tener ese CD como fuente:

```
$ sudo apt-cdrom add
```

  [crear paquetes .deb mediante checkinstall]: {{< relref "/posts/admin/crear-paquetes-deb-con-checkinstall.md" >}}
