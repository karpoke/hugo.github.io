---
title: 'Solucionado el error "Fontconfig warning: reading configurations from ~/.fonts.conf is deprecated." en Ubuntu'
date: 2012-12-23T13:51:00+01:00
categories: ["admin"]
tags: ["12.10", "deprecated", "fontconfig", "quantal quetzal", "ubuntu", "warning"]
slug: "solucionado-el-error-fontconfig-warning-reading-configurations-from-fonts-conf-is-deprecated-en-ubuntu"
---
En Ubuntu, si tenemos el archivo de configuración `~./fonts.conf` y
lanzamos una aplicación que lo utilice, es posible que nos aparezca un
error como el siguiente:

```
Fontconfig warning: "/etc/fonts/conf.d/50-user.conf", line 9: reading configurations from ~/.fonts.conf is deprecated.
```

El motivo, [tal como apunta Githlar en este foro][], es que
`~/.fonts.conf` será eliminado en el futuro. La solución pasa por mover
el fichero a su nuevo emplazamiento (es posible que necesitemos primero
crear el directorio destino):

```
$ mkdir -p .config/fontconfig
$ mv -i ~/.fonts.conf ~/.config/fontconfig/fonts.conf
```

Referencias
-----------

» [Fontconfig warning][]
» [better \~/.fonts.conf deprecation warning][tal como apunta Githlar
en este foro]

  [tal como apunta Githlar en este foro]: http://askubuntu.com/questions/206271/fontconfig-warning
  [Fontconfig warning]: https://bugs.launchpad.net/ubuntu/+source/fontconfig/+bug/1068549
