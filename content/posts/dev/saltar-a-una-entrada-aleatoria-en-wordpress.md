---
title: "Saltar a una entrada aleatoria en WordPress"
date: 2012-07-27T00:20:00+01:00
draft: false
categories: ["dev"]
tags: ["aleatoriedad", "página aleatoria", "php", "wordpress"]
slug: "saltar-a-una-entrada-aleatoria-en-wordpress"
---
Si queremos añadir un enlace que nos permita saltar a una entrada
aleatoria de un blog en WordPress, basta crear un archivo que contenga
lo siguiente:

```
<?php
require('wp-blog-header.php');
query_posts(array('orderby' => 'rand', 'showposts' => 1));
if (have_posts()) : the_post();
$url = get_permalink($post->id);
        header("Location: " . $url);
endif;
wp_reset_query();
?>
```

Guardamos el archivo en una ruta accesible, por ejemplo en la raíz del
blog.

Sólo queda añadir el enlace para que nos lleve a una [entrada
aleatoria][].

PS: Recordando una vieja entrada en [Microsiervos][].

* * * * *

#### Actualizado el 28 de septiembre de 2012

WordPress puede utilizar URLs claras para enlazar a los artículos,
categorías, etiquetas, páginas o archivos. Si queremos que el enlace al
_script_ sea del mismo tipo, podemos añadir las siguientes líneas al
fichero `.htaccess` de la raíz del sitio:

```
RewriteEngine On
RewriteBase /blog/
RewriteRule ^salta/$ salta.php
```

* * * * *

Referencias
-----------

» [Function Reference/query posts][]
» [The Loop][]
» [Template Tags/get posts][]

  [Microsiervos]: http://www.microsiervos.com/archivo/general/salta.html
  [entrada aleatoria]: /salta/
  [Function Reference/query posts]: http://codex.wordpress.org/Function_Reference/query_posts
  [The Loop]: http://codex.wordpress.org/The_Loop
  [Template Tags/get posts]: https://codex.wordpress.org/Function_Reference/get_posts
