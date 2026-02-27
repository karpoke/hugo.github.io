---
title: "Buscando rootkits y troyanos"
date: 2010-12-17T03:04:00+01:00
categories: ["admin"]
tags: ["/dev/.initramfs", "/dev/.udev", "12.04", "13.10", "ALLOWHIDDENFILE", "antirootkit", "chkconfig", "chkrootkit", "e2fsprogs", "ext2", "ext3", "ext4", "lsattr", "python", "reiserfs", "rkhunter", "rootkit", "script", "symlink", "tiger", "troyano", "ubuntu", "unhide", "xfs", "zeppoo"]
slug: "buscando-rootkits-y-troyanos"
---
Tres herramientas muy útiles: `rkhunter`, `chkrootkit` y `unhide`.


rkhunter
--------

Busca _rootkits_, puertas traseras y _exploits_. Al instalarlo, se
programa un escaneo diario, pero cuando instalamos las actualizaciones
de algunos programas, [las firmas de `rkhunter` quedan obsoletas][las firmas de rkhunter quedan obsoletas], por
lo que empieza a mandar avisos.


```
Warning: The file properties have changed:
         File: /usr/bin/md5sum
         Current inode: 1093680    Stored inode: 475456
         Current file modification time: 1285094009 (21-sep-2010 20:33:29)
         Stored file modification time : 1267759792 (05-mar-2010 04:29:52)
```


Podemos actualizar las firmas de `rkhunter` ejecutando:

```
$ sudo rkhunter --propupd
```

El motivo de que no se actualicen las firmas automáticamente es que es
responsabilidad del usuario asegurarse de que los ficheros del sistema
son genuinos y provienen de una fuente fiable. Cuando ejecutamos el
comando anterior, le estamos diciendo a `rkhunter` que acepte las firmas
de los nuevos ficheros como válidas y a éstos como genuinos.

### Directorios o ficheros ocultos

Si usamos Ubuntu, es posible que nos llegue un correo de aviso de
`rkhunter` diciendo que ha encontrado una serie de directorios ocultos,
pero que son legítimos en Ubuntu. Por ejemplo:

```
Warning: Hidden directory found: /dev/.udev
```

Para solucionarlo, editamos el fichero de configuración
`/etc/rkhunter.conf` y descomentamos, o añadimos, las líneas referentes
a dichos directorios:

```
ALLOWHIDDENDIR=/dev/.udev
```

Si en lugar de un directorio es un fichero, la directiva a utilizar es
`ALLOWHIDDENFILE`.

Después de introducir los cambios, actualizamos `rkhunter`:

```
$ sudo rkhunter --propupd
```

* * * * *

#### Actualización a 17 de marzo de 2013

La versión de los repositorios, la 1.3.8, tiene un pequeño fallo por el
cual [los enlaces simbólicos no pueden ser ignorados][] mediante la
directiva `ALLOWHIDDENFILES`, por lo que aparece un mensaje como el
siguiente:

```
Warning: Hidden file found: /dev/.initramfs: symbolic link to `/run/initramf`s
```

En la versión 1.4.0 ya está corregido, aunque aún no se encuentra en los
repositorios en Ubuntu 12.04.2. Una alternativa es [parchear el
script][parchear el _script_].

Editamos el _script_ en Python y vamos a la línea 846:

```
$ sudo vim +846 /usr/bin/rkhunter
```

Justo a continuación, deberemos comprobar si el fichero en un enlace
simbólico, por lo que el código deberá queda así:

```
elif [ -d "${FNAME}" ]; then
    #
    # For the ALLOWHIDDENFILE option we need to allow
    # a hidden symbolic link to a directory.
    #
    test "${OPT_NAME}" = "ALLOWHIDDENFILE" -a -h "${FNAME}" && continue
```

```
    case "${OPT_NAME}" in
```

Ahora ya podemos añadir el fichero en el archivo de configuración
`/etc/rkhunter.conf`:

```
ALLOWHIDDENFILE="/dev/.initramfs"
```

Y actualizar la base de datos de firmas:

```
$ sudo rkhunter --propupd
```

Si usamos algún programa que comprueba la integridad de los ficheros,
como por ejemplo `tiger`, es posible que recibamos una aviso como el
siguiente:

```
NEW: --FAIL-- [lin005f] Installed file '/usr/bin/rkhunter' checksum differs from installed package 'rkhunter'.
```

* * * * *

### Comandos que cambian a _scripts_

Si se añade un _script_ al `PATH` del sistema o sustituye a algún
comando, `rkhunter` también nos lo notificará. Por ejemplo:

```
Warning: The command '/sbin/chkconfig' has been replaced by a script: /sbin/chkconfig: a /usr/bin/perl script text executable
```

Si estamos seguros de que el cambio es legítimos, podemos añadir la
siguiente línea en `/etc/rkhunter.conf`:

```
SCRIPTWHITELIST=/sbin/chkconfig
```

Después de introducir los cambios, actualizamos `rkhunter`:

```
$ sudo rkhunter --propupd
```

### `rkhunter` y `reiserfs`

Si nuestro sistema de ficheros es `reiserfs`, o `xfs`, y hemos instalado
el paquete `e2fsprogs`, el cual contiene herramientas para trabajar con
sistemas de ficheros `ext2`, `ext3` y `ext4`, es posible que recibamos
un aviso que se queja de `lsattr`:

```
Warning: Checking for prerequisites [ Warning ]
No output from the 'lsattr' command - all file immutable-bit checks
will be skipped.
```

La [solución][] pasa por editar el fichero `/etc/rkhunter.conf`, buscar
la directiva `DISABLE_TESTS` y añadir el parámetro `immutable` al final.

A continuación, actualizamos `rkhunter`:

```
$ sudo rkhunter --propupd
```

chkrootkit
----------

...detecta _rootkits_. Por defecto, sólo se ejecuta cuando lo lanzamos
nosotros. Para que se realice un escaneo diario, modificaremos el
fichero `/etc/chkrootkit.conf`:

```
RUN_DAILY="true"
```

* * * * *

#### Actualizado el 2 de noviembre de 2013

En los reportes de `chkrootkit` es posible que nos llegue el aviso de
que el archivo `/sbin/init` está infectado:

```
Warning: /sbin/init INFECTED
```

Parece ser un [fallo en `chkrootkit`][fallo en chkrootkit], ya que para determinar si el
archivo `/sbin/init` está infectado, lo que hace es buscar la cadena
"HOME" el el fichero, mediante el comando `strings`:

```
$ strings /sbin/init | egrep HOME
XDG_CACHE_HOME
XDG_CONFIG_HOME
```

El fallo está presente al menos en la versión 0.49, que es la que hay
disponible en los repositorios de Ubuntu Saucy Salamander. Una manera de
evitar el aviso es buscar el siguiente trozo de código, alrededor de la
línea 1005:

```
if [ ${SYSTEM} != "HP-UX" ] && ( ${strings} ${ROOTDIR}sbin/init | ${egrep} HOME  ||
     cat ${ROOTDIR}/proc/1/maps | ${egrep} "init." ) >/dev/null 2>&1
```

Y sustituirlo por:

```
if [ ${SYSTEM} != "HP-UX" ] && ( cat ${ROOTDIR}/proc/1/maps | ${egrep} "init." ) >/dev/null 2>&1
```

* * * * *

unhide
------

Detecta procesos ocultos y puertas traseras, [basándose en la
información][] obtenida de `/proc`, `/bin/ps` y `syscalls`, y de los
puertos activos que no aparecen según `/bin/netstat`.

En la versión [unhide-20100201-1][], para el listado de procesos,
comprueba los resultados de `/bin/ps`, ejecutándolo de las siguientes
maneras:

```
// we are looking only for real process not thread and only one by one
#define COMMAND "ps --no-header -p %i o pid"
// we ara looking for session ID one by one
#define SESSION "ps --no-header -s %i o sess"
// We are looking for group ID one by one
// but ps can’t select by pgid
#define PGID "ps --no-header -eL o pgid"
// We are looking for all processes even threads
#define THREADS "ps --no-header -eL o lwp"
// for sysinfo scanning, fall back to old command, as --no-header seems to create
// an extra process
#define SYS_COMMAND "ps -eL o lwp"
```

En escaneo de puertos utiliza los resultados de `/bin/netstat`:

```
// Linux
char tcpcommand[]= "netstat -tan | sed -e '/[\\.:][0-9]/!d' -e 's/.*[\\.:]\\([0-9]*\\) .*[\\.:].*/\\1/'" ;
char udpcommand[]= "netstat -uan | sed -e '/[\\.:][0-9]/!d' -e 's/.*[\\.:]\\([0-9]*\\) .*[\\.:].*/\\1/'" ;
```

Podemos lograr [que se ejecute periódicamente][] añadiendo al `crontab`
algo como:

```
0  8 * * * unhide-linux26 proc 2>&1 | mail -s "Daily unhide-linux26 proc Scan" user@example.com
30 8 * * * unhide-linux26 sys 2>&1 | mail -s "Daily unhide-linux26 sys Scan" user@example.com
0  9 * * * unhide-linux26 brute 2>&1 | mail -s "Daily unhide-linux26 brute Scan" user@example.com
30 9 * * * unhide-tcp 2>&1 | mail -s "Daily unhide-tcp Scan" user@example.com
```

  [las firmas de rkhunter quedan obsoletas]: http://www.mail-archive.com/rkhunter-users@lists.sourceforge.net/msg01966.html
  [los enlaces simbólicos no pueden ser ignorados]: https://bugs.launchpad.net/ubuntu/+source/rkhunter/+bug/883324
  [parchear el script]: https://bugs.launchpad.net/ubuntu/+source/rkhunter/+bug/883324/comments/13
  [solución]: http://blog.unixum.de/tiki-index.php?page=install+rkhunter+-+debian+lenny
  [fallo en chkrootkit]: https://bugzilla.redhat.com/show_bug.cgi?id=636231
  [basándose en la información]: http://www.securitybydefault.com/2008/06/detectando-la-presencia-de-rootkits-con.html
  [unhide-20100201-1]: http://unhide.sourcearchive.com/documentation/20100201-1/
  [que se ejecute periódicamente]: http://samiux.wordpress.com/2009/06/13/howto-make-sure-no-rootkit-on-your-ubuntu-9-04-server/
