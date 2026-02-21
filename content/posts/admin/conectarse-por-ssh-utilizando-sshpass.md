---
title: "Conectarse por SSH utilizando sshpass"
date: 2013-06-09T15:47:00+01:00
draft: false
categories: ["admin"]
tags: ["contraseña", "ssh", "sshpass"]
slug: "conectarse-por-ssh-utilizando-sshpass"
---
`sshpass` es un programa que nos permite iniciar sesión en un servidor
SSH de forma no interactiva y sin utilizar claves, para lo que deberemos
proporcionar la contraseña como argumento del programa.

Para conectar a un servidor SSH, es preferible [utilizar claves][],
además de tener en cuenta otros sistemas de seguridad, como la
[autenticación en dos pasos][], pero puede haber escenarios en los que
`sshpass` sea una alternativa a considerar.

Su uso es sencillo:

```
$ sshpass -p password ssh example.com
```

El hecho de que la contraseña se escriba directamente en el terminal,
además de que es posible que [quede escrita en el historial][], podría
hacer que fuese visible al ejecutar otro usuario el comando `ps`. Sin
embargo, `sshpass` se encarga de sustituir la contraseña por zetas:

```
$ ps a | grep sshpass
18998 pts/6    S+     0:00 sshpass -p zzzzzzzz ssh example.com
```

Referencias
-----------

» [sshpass: Login To SSH Server / Provide SSH Password Using A Shell
Script][]

  [utilizar claves]: {{< relref "/posts/admin/conectarse-por-ssh-solo-usando-la-clave.md" >}}
  [autenticación en dos pasos]: {{< relref "/posts/admin/servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal.md" >}}
  [quede escrita en el historial]: {{< relref "/posts/admin/evitar-el-registro-de-comandos-en-el-historial.md" >}}
  [sshpass: Login To SSH Server / Provide SSH Password Using A Shell Script]: http://www.cyberciti.biz/faq/noninteractive-shell-script-ssh-password-provider/
