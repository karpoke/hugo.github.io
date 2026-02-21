---
title: "Actualizando Ubuntu a la última distribución de forma remota"
date: 2011-01-07T04:38:00+01:00
draft: false
categories: ["admin"]
tags: ["10.04", "10.10", "actualización", "do-release-upgrade", "ubuntu lucid lynx", "ubuntu maverick meerkat", "update-manager"]
slug: "actualizando-ubuntu-a-la-ultima-distribucion-de-forma-remota"
---
Instalamos el paquete `update-manager`, si es que no lo teníamos:

```
$ sudo aptitude install update-manager
```

Comprobamos que el fichero `/etc/update-manager/release-upgrades`
contiene:

```
Prompt=normal
```

Si contiene `Prompt=lts` sólo nos actualizará si hay una [LTS][] nueva.
Si contiene `Prompt=never`... no actualizará nada.

![Ape Man Evolution]({static}/images/ape_man_evolution.png)

Y ejecutamos el comando `do-release-upgrade`:

```
$ sudo do-release-upgrade
```

» [ubuntugeek][]

  [LTS]: http://es.wikipedia.org/wiki/Ubuntu
  [ubuntugeek]: http://www.ubuntugeek.com/how-to-upgrade-from-ubuntu-10-04-lucid-to-ubuntu-10-10-maverick-desktop-and-server.html
