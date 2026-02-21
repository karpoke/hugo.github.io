---
title: "Facebook y el RSS de las páginas"
date: 2011-10-10T17:05:00+01:00
draft: false
categories: ["hack"]
tags: ["atom", "facebook", "feed", "rss"]
slug: "facebook-y-el-rss-de-las-paginas"
---
Si queremos [seguir las actualizaciones de una página de Facebook][], no
tenemos más que copiar el ID de la página y sustituirlo en la siguiente
URL, en este caso en formato Atom 1.0:

```
http://www.facebook.com/feeds/page.php?format=atom10&id=xxxxxxxxxxxx
```

O la siguiente, para usar el formato RSS 2.0:

```
http://www.facebook.com/feeds/page.php?format=rss20&id=xxxxxxxxxxxx
```

Por ejemplo, para añadir el RSS de la página de Amstrad ESP,
[http://www.facebook.com/pages/Amstrad-ESP/__72227918057__][], no
tenemos más que utilizar la siguiente URL:

[http://www.facebook.com/feeds/page.php?format=rss20&id=__72227918057__][]

  [seguir las actualizaciones de una página de Facebook]: http://rubenbaston.org/rss-paginas-facebook/
  [http://www.facebook.com/pages/Amstrad-ESP/__72227918057__]: http://www.facebook.com/pages/Amstrad-ESP/72227918057
  [http://www.facebook.com/feeds/page.php?format=rss20&id=__72227918057__]:
```
http://www.facebook.com/feeds/page.php?format=rss20&id=72227918057
"Amstrad ESP. Facebook Page RSS"
```
