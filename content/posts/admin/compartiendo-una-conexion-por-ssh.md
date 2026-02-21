---
title: "Compartiendo una conexión por SSH"
date: 2011-06-17T15:28:00+01:00
draft: false
categories: ["admin"]
tags: ["compartir", "openssh", "ssh"]
slug: "compartiendo-una-conexion-por-ssh"
---
A partir de la versión 4 de OpenSSH se pueden [compartir las conexiones
seguras][] a un máquina remota, de tal manera que, una vez establecida
la primera conexión, el resto de conexiones reutilizan la primera, por
lo que el establecimiento de la conexión de éstas será mucho más rápido.


Configuración
-------------

Lo primero es asegurarnos de que existe el directorio `~/.ssh` en el
cliente, con permisos 700 (sólo accesible por nosotros mismos... y
cualquier administrador).

A continuación, añadimos las siguientes líneas al fichero
`~/.ssh/config`:

```
Host *
ControlPath ~/.ssh/master-%l-%r@%h:%p
ControlMaster auto
```

-   `Host *` especifica que se aplica a cualquier máquina remota,
-   `ControlMaster auto` especifica que se reutilice una conexión
```
existente, si es posible, y
```
-   `ControlPath ~/.ssh/master-%l-%r@%h:%p` especifica dónde se debe
```
crear el fichero de _socket_ que representa la conexión maestra.
`%r` se sustituye por el nombre de usuario, `%h` por el nombre de la
máquina remota, `%p` por el puerto remoto y `%l` por el nombre de la
máquina local, que, aunque sólo es útil si el directorio se puede
montar en varias máquinas (por ejemplo, si el directorio de usuario
se monta por NFS), no molesta si se incluye siempre.
```

Comparación de tiempos
----------------------

Para la primera conexión:

```
$ time ssh user@remote exit
real    0m1.217s
user    0m0.012s
sys     0m0.004s
```

Para las siguientes conexiones:

```
$ time ssh user@remote exit
real    0m0.168s
user    0m0.008s
sys     0m0.012s
```

La diferencia es notable. Para evitar que nos pida la contraseña y tener
que introducirla manualmente, podemos utilizar el [inicio de sesión por
clave][], o recurrir al [comando `expect` para evitar introducir la
contraseña][comando expect para evitar introducir la contraseña].

Las siguientes conexiones
-------------------------

Si estamos haciendo estas pruebas utilizando algunos de los _scripts_
que se basan en `expect` es posible que nos de un error o un al intentar
enviar la contraseña, ya que mientras estemos haciendo uso de la
conexión compartida, para las siguientes conexiones no será necesario
introducir la contraseña.

Ademá, dado que se reutiliza la conexión maestra, si queremos
conectarnos utilizando diferentes parámetros deberemos crear una
conexión nueva, utilizando el argumento `-S none`:

```
$ ssh -S none -X user@remote
```

Ficheros de `socket`
--------------------

Si no finalizamos la conexión correctamente, es posible que el fichero
de _socket_ no se elimine correctamente, lo que puede provocar que no
nos permita volver a conectarnos:

```
Control socket connect(/home/user/.ssh/master-remote-local@example.net:1234): Connection refused
ControlSocket /home/user/.ssh/master-remote-local@example.net:1234 already exists
```

Simplemente debemos eliminar estos ficheros para solucionarlo.

Salir de la sesión maestra mientras hay otras conexiones
--------------------------------------------------------

Si salimos de la sesión maestra mientras hay más conexiones abiertas, la
primera quedará colgada hasta que terminen el resto de sesiones. Una
posible solución para evitar este inconveniente es realizar la conexión
maestra utilizando el argumento `-N` para que no nos ofrezca un terminal, y
matar el proceso cuando ya no la necesitemos.

  [compartir las conexiones seguras]: http://protempore.net/~calvins/howto/ssh-connection-sharing/
  [inicio de sesión por clave]: {{< relref "/posts/admin/conectarse-por-ssh-solo-usando-la-clave.md" >}}
  [comando expect para evitar introducir la contraseña]: {{< relref "/posts/admin/conectarse-por-ssh-utilizando-expect.md" >}}
