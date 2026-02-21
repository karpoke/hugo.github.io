---
title: "sudo vacilón"
date: 2011-08-04T13:32:00+01:00
draft: false
categories: ["admin"]
tags: ["sudo", "sudo rm -fr", "visudo"]
slug: "sudo-vacilon"
---
```
$ sudo passwd
[sudo] password for user:
Are you on drugs?
[sudo] password for user:
Maybe if you used more than just two fingers...
[sudo] password for user:
I’ve seen penguins that can type better than that.
sudo: 3 incorrect password attempts
```

Si te gustaría recibir un piropo cada vez que [escribes mal la
contraseña de `sudo`][escribes mal la contraseña de sudo], no
tienes más que editar el archivo de configuración de [`sudo`][sudo],
`/etc/sudoers`, mediante el comando `visudo`:

```
$ sudo visudo
```

Y añadir la opción `insults`:

```
Defaults        env_reset,insults
```

  [escribes mal la contraseña de sudo]: http://usemoslinux.blogspot.com/2011/08/sudo-no-me-insultes-el-terminal-se.html
  [sudo]: /posts/memo/with-great-power-comes-great-responsibility/
