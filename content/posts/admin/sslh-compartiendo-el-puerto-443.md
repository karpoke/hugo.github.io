---
title: "sslh, compartiendo el puerto 443"
date: 2011-07-30T19:21:00+01:00
draft: false
categories: ["admin"]
tags: ["apache", "firewall", "https", "logcheck", "puertos bien conocidos", "ssh", "ssl", "sslh", "ufw"]
slug: "sslh-compartiendo-el-puerto-443"
---
Podemos tener varios motivos para tener escuchando nuestro servicio de SSH en
el puerto 443. Ya sea porque queremos evitarnos los continuos intentos de
conexión que sufrimos por tener el servicio escuchando en el puerto 22 o porque
desde donde estemos, ya sea en el trabajo o en un hotel, no estén permitidas
las conexiones que no sean al puerto 80 o 443. Pero, ¿y si [ya tenemos un
servidor web][] escuchando en el puerto 443?

Mediante `sslh` se puede multiplexar la conexión al puerto 443, de tal forma
que dependiendo del protocolo utilizado para conectarnos reenvíe la conexión al
puerto 22 si es SSH o al 443 si es SSL. La detección del protocolo se basa en
los primeros bytes enviados por el cliente. Las conexiones SSH empiezan con la
identificación del cliente utilizando la cadena "SSH-2.0", dependiendo de la
versión. Los clientes OpenVPN cmoienzan con 0x00 0x0D 0x38. Hay dos tipos de
clientes SSH, los que esperan que sea el servidor el primero que envíe su
versión (_shy client_) y los que son ellos los que la envían primero (_bold
client_).

`sslh` espera un tiempo para recibir la versión de SSH. Si transcurrido ese
tiempo no ha recibido nada, asume que es un "cliente tímido" y se realiza la
conexión con el servidor SSH. Si el cliente envía un paquete antes, `sslh` lo
lee y se lo envía al servidor SSH o SSL, según corresponda.

Uno de los inconvenientes de `sslh` es que tanto el servidor de SSH como el
servidor web no ven la IP original, ya que la conexión se redirecciona desde
`sslh`. Para poder limitar el acceso, `sslh` se puede compilar para que
compruebe las listas de acceso definidas en `/etc/hosts.allow` y
`/etc/hosts.deny`.


Instalación desde los respositorios de Ubuntu Lucid Lynx
--------------------------------------------------------

Lo podemos instalar desde los respositorios. Es Ubuntu Lucid Lynx está la
versión 1.6i-4:

```
$ sudo aptitude install sslh
```

Al principio, se encuentra desactivado, para obligarnos a leer la
documentación. Después de echarle un ojo a la página del `man`, podemos
configurarlo editando el fichero `/etc/default/sslh`:

```
DAEMON_OPTS="-u sslh -p 0.0.0.0:443 -s 127.0.0.1:22 -l 127.0.0.1:1443 -P /var/run/sslh.pid"
RUN=yes
```

Estas opciones indican que el servicio se ejecutará como el usuario
`sslh`, escuchando en todas las interfaces en el puerto 443, y
redireccionará las conexiones SSH al puerto 22 de la máquina local, y
las conexiones SSL al puerto 1443 de la máquina local. El archivo que
contiene el PID del servicio es `/var/run/sslh.pid`. Para que pueda
ejecutarse, debemos añadir la última línea, `RUN=yes`.

Instalación desde el código fuente
----------------------------------

Ahora mismo van por la versión 1.9, así que en lugar de instalarlo desde los
repositorios, lo haremos desde el código fuente:

```
$ wget http://www.rutschle.net/tech/sslh-1.9.tar.gz
$ tar xzvf sslh-1.9.tar.gz
$ cd sslh-1.9/
```

Si queremos compilar con la opción de que se comprueben las listas de acceso,
deberemos realizar un par de acciones previas al `make install`:

```
$ sudo aptitude install libwrap0{,-dev} tcpd
$ sed -i 's/USELIBWRAP=./USELIBWRAP=1/' Makefile
```

Ahora ya podemos pasar a la instalación:

```
$ sudo make install
$ sudo make install-debian
```

Editamos el fichero `/etc/default/sslh` para configurar las interfaces.  Para
evitar que haya cualquier tipo de colisión entre `openssh`, `apache2` y `sslh`,
debemos asegurarnos de que no escuchan en el mismo puerto o que lo hacen en
interfaces diferentes. En la interfaz en la que escucha `sslh` podríamos poner
nuestra IP pública, si fuese fija. Sino, lo más cómodo será cambiar el puerto
en el que escucha `apache2` para las conexiones seguras:

```
LISTEN=0.0.0.0:443
SSH=localhost:22
SSL=localhost:1443
```

Configurar `apache2`
--------------------

Antes de reiniciar el servicio `sslh`, deberemos modificar la configuración de
Apache para que no haya conflicto entre las interfaces.  En el fichero
`/etc/apache2/ports.conf` cambiamos el número de puerto en el que escucha para
[las conexiones seguras][]:

```
Listen 1443 # formerly 443
```

No olvidemos cambiarlo también en la configuración del `VirtualHost`, por
ejemplo en `/etc/apache2/sites-available/default-ssl`.

Ahora, reiniciamos ambos servicios:

```
$ sudo service sslh start
$ sudo service apache2 restart
```

Ya podemos probarlo.

```
$ w3m https://mydomain.com
$ ssh -p443 mydomain.com
```

En los _logs_, `/var/log/syslog`, podremos ver algo como:

```
Jul 30 19:38:00 terminus sslh[25196]: connection from 1.2.3.4:42711 forwarded to SSL
Jul 30 19:38:01 terminus sslh[25196]: connection from 1.2.3.4:42712 forwarded to SSL
Jul 30 19:39:01 terminus sslh[25196]: connection from 1.2.3.4:43923 forwarded to SSH
```

`logcheck` nos alerta de cada conexión redirigida
-------------------------------------------------

Si tenemos instalado [`logcheck`][logcheck] y [no queremos que nos lleguen
estos avisos][] cada vez, podemos crear el archivo
`/etc/logcheck/ignore.d.server/sslh` e incluir la siguiente línea:

```
^\w{3} [ :[:digit:]]{11} [._[:alnum:]-]+ sslh\[[[:digit:]]+\]: connection from [:.[:xdigit:]]+ forwarded to SS(L|H)$
```

¿Y el cortafuegos?
------------------

Si, por ejemplo, utilizamos [`ufw`][logcheck], podemos modificar la [regla para
permitir las conexiones][] al puerto 22 únicamente desde la propia LAN:

```
$ sudo ufw allow proto tcp from 192.168.50.0/24 to any port 22
```

También podemos borrar la regla antigua:

```
$ sudo ufw delete allow tcp/22
```

  [ya tenemos un servidor web]: http://dischord.org/blog/2010/08/25/multiplexing-ssh-and-ssl/
  [las conexiones seguras]: {{< relref "/posts/admin/configurar-apache-para-servir-conexiones-seguras.md" >}}
  [logcheck]: {{< relref "/posts/admin/detectando-intrusos-en-ubuntu-maverick-meerkat.md" >}}
  [no queremos que nos lleguen estos avisos]: {{< relref "/posts/admin/kernel-time-sync-status-change.md" >}}
  [regla para permitir las conexiones]: http://pka.engr.ccny.cuny.edu/~jmao/node/28
