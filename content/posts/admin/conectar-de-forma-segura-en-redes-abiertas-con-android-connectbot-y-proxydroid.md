---
title: "Conectar de forma segura en redes abiertas con Android, ConnectBot y ProxyDroid"
date: 2012-07-24T14:02:00+01:00
categories: ["admin"]
tags: ["android", "connectbot", "proxy", "proxy transparente", "proxydroid", "seguridad en redes inalámbricas", "ssh", "túnel ssh"]
slug: "conectar-de-forma-segura-en-redes-abiertas-con-android-connectbot-y-proxydroid"
---
Si necesitamos conectarnos desde nuestro terminal con Android a una red
WiFi que no es segura, ya sea porque es una red abierta o porque no es
de confianza, podemos utilizar ConnectBot para crear un túnel SSH para
encauzar todas las conexiones que realicemos desde el terminal a través
de él.

Para esto necesitaremos:

-   Acceso a un servidor SSH
-   Un cliente SSH para Android, por ejemplo ConnectBot
-   Un cliente proxy para Android, por ejemplo ProxyDroid

[ProxyDroid][] es una aplicación que permite crear un _proxy_
transparente en terminales Android.

Si queremos que todas las conexiones vayan a través del _proxy_ de forma
transparente, es decir, sin tener que configurar nada más en el terminal
ni en las aplicaciones, necesitaremos que el terminal esté _rooteado_.

El primer paso será [conectarnos con ConnectBot al servidor SSH mediante
claves][], para evitar tener que estar introduciendo contraseñas, de tal
manera que con añadir un _widget_ la conexión se realizará con una sólo
pulsación.

Para crear la redirección de puertos en ConnectBot, realizamos una
pulsación larga sobre la conexión a utilizar, que ya debemos tener
configurada previamente, y seleccionamos Editar redirección de puertos.
Pulsamos en Menú > Añadir redirección de puertos y utilizamos los
siguientes datos:

-   Nombre: el nombre que le damos a esta redirección de puertos (puede
```
ser cualquiera)
```
-   Tipo: Dinámico (SOCKS)
-   Puerto fuente: 3128 (es el que utiliza ProxyDroid por defecto)
-   Destino: no es relevante

En ProxyDroid, deberemos utilizar los siguientes datos:

-   Host: localhost
-   Puerto: 3128
-   Proxy Type: SOCKS5
-   Global Proxy: Lo marcamos para que todas las peticiones vayan por el
```
_proxy_. Necesitaremos que el teléfono esté _rooteado_
```

Añadimos un _widget_ para facilitar la activación del _proxy_.

De esta forma, para conectarnos a una red WiFi insegura:

1.  activamos el _proxy_ antes de conectarnos
2.  nos conectamos a la red WiFi
3.  creamos el túnel SSH conectándonos al servidor remoto

Si la red WiFi tiene un portal cautivo, deberemos conectarnos antes de
activar el _proxy_ y acceder mediante el navegador para introducir la
contraseña o aceptar las condiciones del servicio, ya que de lo
contrario no podremos conectarnos al servidor SSH (a no ser que
encontremos una manera de [saltarnos dicho portal cautivo][]).

Referencias
-----------

» [ConnectBot][] en el _market_
» [ProxyDroid][1] en el _market_

  [ProxyDroid]: http://code.google.com/p/proxydroid/
  [conectarnos con ConnectBot al servidor SSH mediante claves]: {{< relref "/posts/admin/conectar-a-un-servidor-ssh-desde-android-mediante-connectbot-utilizando-claves.md" >}}
  [saltarnos dicho portal cautivo]: /posts/hack/saltandonos-el-portal-cautivo-de-una-biblioteca/
  [ConnectBot]: http://play.google.com/store/apps/details?id=org.connectbot
  [1]: http://play.google.com/store/apps/details?id=org.proxydroid

