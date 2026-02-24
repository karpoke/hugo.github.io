---
title: "ownCloud con MySQL en Ubuntu Lucid Lynx 10.04"
date: 2012-05-10T16:17:00+01:00
categories: ["admin"]
tags: ["10.04", "https", "mysql", "nautilus", "nube", "owncloud", "soberanía de datos", "ubuntu lucid lynx", "webdav"]
slug: "owncloud-con-mysql-en-ubuntu-lucid-lynx-10-04"
---
![Owncloud logo]({static}/images/owncloud-logo-300x148.png)

[ownCloud][] es una aplicación de código abierto que nos facilita tener
nuestra propia nube, permitiendo guardar, sincronizar y compartir todo
tipo de archivos, incluyendo imágenes, música y vídeos. También tenemos
la posibilidad de incluir [aplicaciones de terceros][] tales como un
calendario, un gestor de contactos, un editor de texto, gestión de
enlaces, etc.

![Owncloud files]({static}/images/owncloud-files-300x119.png)

Para instalarlo en Ubuntu Lucid Lynx 10.04, seguiremos los siguientes
pasos.

Instalamos las dependencias, incluyendo algunas opcionales:

```
$ sudo aptitude install apache2 php5 php-pear php-xml-parser php5-json zip php5-gd php5-sqlite sqlite php5-mysql id3v2 curl libcurl3 libcurl4-openssl-dev php5-curl
```

Descargamos la última versión estable, en estos momentos 3.0.3:

```
$ wget http://owncloud.org/releases/owncloud-3.0.3.tar.bz2
```

Comprobamos el MD5:

```
$ md5sum owncloud-3.0.3.tar.bz2
01300ca8b8be549af166f568fef8538f  owncloud-3.0.3.tar.bz2
$ wget -qO - http://owncloud.org/releases/owncloud-3.0.3.tar.bz2.md5
01300ca8b8be549af166f568fef8538f  owncloud-3.0.3.tar.bz2
```

Descomprimimos el fichero:

```
$ tar -xjf owncloud-3.0.3.tar.bz2
```

Lo movemos al `DocumentRoot`:

```
$ sudo mv owncloud /var/www/
```

Le cambiamos el propietario a los ficheros:

```
$ sudo chown -R www-data:www-data /var/www/owncloud
```

Creamos la base de datos y el usuario en MySQL:

```
$ mysql -uroot -p
mysql> CREATE DATABASE owncloud;
mysql> CREATE USER 'owncloud'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON owncloud.* TO 'owncloud'@'localhost';
mysql> FLUSH PRIVILEGES;
```

Nos aseguramos de tener habilitado `.htaccess` en Apache. Basta
comprobar que en el fichero de configuración del sitio, la directiva
`AllowOverride` para el `DocumentRoot` es `All`.

También deberán estar instalados y activados los módulos `mod_headers`,
`mod_rewrite` y `mod_env` en Apache:

```
$ sudo a2enmod headers
$ sudo a2enmod rewrite
$ sudo a2enmod env
```

Reiniciamos Apache:

```
$ sudo apache2ctl restart
```

Ya podemos acceder al panel de administración de ownCloud en
`http://localhost/owncloud`. Creamos el usuario administrador y
configuramos los valores de hemos utilizado en MySQL.

* * * * *

#### Actualizado el 28 de julio de 2012

### Atención: Es necesario mover el directorio `data` fuera del `DocumentRoot`

A partir de la versión 4.0.5, si utilizamos un directorio de datos que
se encuentre dentro del `DocumentRoot`, al abrir la pestaña de
Administración encontraremos algo como esto:

> *Your data directory and your files are probably accessible from the
> internet. The .htaccess file that ownCloud provides is not working. We
> strongly suggest that you configure your webserver in a way that the
> data directory is no longer accessible or you move the data directory
> outside the webserver document root.*

Tal como indica, el contenido del directorio `data` puede que sea
accesible desde fuera de la red. No podremos obtener un listado de los
ficheros que contiene, pero si supiéramos el nombre de algún fichero sí
que podríamos descargarlo directamente, **de cualquier usuario, incluso
sin haber iniciado sesión**.

Para evitarlo, moveremos el directorio `data` a cualquier otro
directorio que esté fuera del `DocumentRoot`, conservando los permisos
que tenía, y acto seguido modificamos el fichero de configuración
`owncloud/config/config.php`:

```
"datadirectory" => '/new/path/to/data',
```

Sólo queda reiniciar el servidor para que los cambios tengan efecto:

```
$ sudo apache2ctl restart
```

* * * * *

Acceso mediante Nautilius y WebDAV
----------------------------------

ownCloud lleva incluido un servidor WebDAV, por lo que podemos acceder
desde Nautilus y montar el directorio. En Nautilus, vamos a Archivo >
Conectar al servidor y además de nuestro usuario y contraseña, ponemos
los siguientes datos:

-   Server: localhost/owncloud
-   Folder: /files/webdav.php

Acceso seguro mediante HTTPS
----------------------------

Si queremos obligar a que el acceso a ownCloud se haga [a través de una
conexión segura][], podemos editar el fichero `.htaccess` del directorio
`/var/www/owncloud` para que contenga:

```
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
RewriteRule .* - [env=HTTP_AUTHORIZATION:%{HTTP:Authorization},last]
```

Actualizaciones
---------------

Instalar una actualización es tan sencillo como reemplazar los ficheros.
Los directorios `config/` y `data/` no se verán afectados, por lo que no
perderemos nuestros datos. La actualización se llevará a cabo cuando
iniciemos sesión como administrador.

* * * * *

#### Actualizado el 24 de mayo de 2012

Acaba de salir la versión estable 4.0.0. Entre las [mejoras de la
versión 4.0.0][] se encuentra el cifrado de archivos, cargar archivos
arrastrando los ficheros, visor de ficheros ODF y muchas más.

Para actualizar, simplemente descargamos la versión y la descomprimimos
en el mismo directorio de instalación:

```
$ wget http://owncloud.org/releases/owncloud-4.0.0.tar.bz2
```

Comprobamos el MD5:

```
$ md5sum owncloud-4.0.0.tar.bz2
440837c2b4908a2ec06f96978d6b7525  owncloud-4.0.0.tar.bz2
$ wget -qO - http://owncloud.org/releases/owncloud-4.0.0.tar.bz2.md5
440837c2b4908a2ec06f96978d6b7525  owncloud-4.0.0.tar.bz2
```

Descomprimimos el fichero:

```
$ tar -xjf owncloud-4.0.0.tar.bz2
```

Le cambiamos el propietario a los ficheros:

```
$ sudo chown -R www-data:www-data owncloud
```

Lo copiamos al `DocumentRoot`:

```
$ cd owncloud
$ sudo cp -r * /var/www/owncloud/
```

Reiniciamos el Apache:

```
$ sudo apache2ctl restart
```

Al iniciar sesión como administrador se lleva a cabo la actualización.

Si nos encontramos con que nuestras canciones, marcadores o [archivos
han desaparecido][], es posible que le lleve un tiempo a la aplicación
escanear el contenido, podemos probar a cerrar sesión y volver a entrar,
escanear de nuevo en busca de los ficheros o incluso volver a reiniciar
el Apache.

* * * * *

Instalar aplicaciones
---------------------

Para instalar una aplicación, la descargamos y la copiamos al directorio
`apps` dentro de `owncloud`. Por ejemplo, la aplicación Files Move
muestra permite mover los archivos de sitio desde la aplicación.

Para instalarlo:

```
$ wget http://apps.owncloud.com/CONTENT/content-files/150271-files_mv.0.21.tgz
$ tar xvzf 150271-files_mv.0.21.tgz
$ sudo mv files_mv/ /var/www/owncloud/apps/
$ sudo chown  -R www-data:www-data /var/www/owncloud/apps/
```

Ahora deberemos activar la aplicación desde el panel de administración
de ownCloud.

### Problemas al instalar algunas aplicaciones

He tenido algún que otro problema instalando alguna aplicación, por
ejemplo la anterior. La activación de la aplicación en el panel de
control no se queda de forma permanente, sino que nada más recargar la
página ésta vuelve a estar desactivada. Parece que es un [fallo
conocido][].

Después de haber descomprimido, movido y cambiado el propietario de la
aplicación, creamos el fichero `/var/www/owncloud/refresh_apps.php`, tal
como sugiere _sshambar_:

```
<?php
$RUNTIME_NOAPPS = TRUE; //no apps, yet
```

```
require_once('lib/base.php');
```

```
// Setup required :
$not_installed = !OC_Config::getValue('installed', false);
if($not_installed) {
header("Location: ".OC::$WEBROOT.'/');
exit();
}
OC_Installer::installShippedApps();
echo(json_encode('Apps updated!'));
?>
```

Accedemos al fichero desde el navegador mediante
`http://localhost/owncloud/refresh_apps.php`, y creará las entradas en
la tabla `oc_appconfig` de la base de datos.

Aún así, esto no ha sido suficiente, ya que en dicha tabla quedaba
registrada como instalada pero no activada, y seguía sin poder activarla
desde el administrador, así que he probado a actualizar la base de datos
de forma directa y me ha funcionado, pero no estoy seguro de que esto
funcione en todos los casos ni de que no entrañe ningún tipo de riesgo.
Así es como he logrado instalar File Move:

```
$ mysql -uowncloud -p owncloud
mysql> update oc_appconfig set configvalue="yes" where appid="storage_charts-v2.0" and configkey="enabled";
```

Sin embargo, con la aplicación Storage Chart v2, que muestra el espacio
utilizado por nuestros ficheros en la nuestra nube, lo anterior no me ha
funcionado y la aplicación daba error, ni siquiera dejaba acceder al
panel de administración, por lo que he tenido que deshacer los cambios.

Referencias
-----------

» [ownCloud site][ownCloud]
» [ownCloud support][]
» [ownCloud apps][aplicaciones de terceros]
» [ownCloud 2, your personal cloud server][]

  [ownCloud]: http://owncloud.org/
  [aplicaciones de terceros]: http://apps.owncloud.com/
  [a través de una conexión segura]: {{< relref "/posts/admin/forzar-el-uso-de-sslhttps-de-un-directorio-en-apache2-mediante-htaccess-y-mod_rewrite.md" >}}
  [mejoras de la versión 4.0.0]: http://owncloud.org/features/
  [archivos han desaparecido]: http://forum.owncloud.org/viewtopic.php?f=3&t=2536
  [fallo conocido]: http://forum.owncloud.org/viewtopic.php?f=3&t=1880#p2702
  [ownCloud support]: http://owncloud.org/install>Install%20ownCloud</a><br%20/>%0A»%20<a%20href=
  [ownCloud 2, your personal cloud server]: http://www.webupd8.org/2011/10/owncloud-2-your-personal-cloud-server.html
