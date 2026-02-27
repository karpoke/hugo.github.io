---
title: "CSRF en las búsquedas de Google"
date: 2010-12-13T14:31:00+01:00
categories: ["hack"]
tags: ["csrf", "google"]
slug: "csrf-en-las-busquedas-de-google"
---
> No se ha encontrado ningún resultado

![No injury is acceptable](/images/no-injury-is-acceptable-300x233.jpg)


Si ahora mismo tienes una sesión de Google iniciada, puedes ir al
[histórico de búsquedas de Google][] y verás que aparece una búsqueda
que no has realizado... conscientemente.

El truco, un ataque [CSRF][] comentado por [Jeremiah Grossman][],
consiste en añadir en el código HTML de la página una imagen cuyo `src`
sea la URL de la búsqueda que queramos que realice el que visite la
página. Por ejemplo:

`<img src="http://www.google.es/search?q=%22terminus.ignaciocano.com%22">`

```
`<img src="http://www.google.es/search?q=%22terminus.ignaciocano.com%22">`
```

  [histórico de búsquedas de Google]: http://google.com/history
  [CSRF]: http://en.wikipedia.org/wiki/Cross-site_request_forgery
  [Jeremiah Grossman]: http://jeremiahgrossman.blogspot.com/2010/12/spoofing-google-search-history-with.html
