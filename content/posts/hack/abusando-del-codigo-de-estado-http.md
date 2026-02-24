---
title: "Abusando del código de estado HTTP"
date: 2011-02-22T17:02:00+01:00
categories: ["hack"]
tags: ["facebook", "fingerprinting", "gmail", "twitter"]
slug: "abusando-del-codigo-de-estado-http"
---
```javascript
function logged_in(id, txt) {
   document.getElementById(id).innerHTML = txt;
}

En el artículo original, de [Mark Cardwell][], se muestra como podemos
saber si un visitante de nuestra página está conectado a diferentes
servicios, como GMail, Facebook, Twitter, etc, aprovechando las
diferencias de comportamiento que muestran estos servicios al acceder a
enlaces concretos si el usuario está conectado o no.


GMail
-----

Conectado a GMail? __**...**__

Para comprobar si el visitante está conectado a GMail se intenta cargar
una imagen de la siguiente manera:


```

```

```

El `src` de la imagen hace referencia a la imagen del perfil de Mark, si
no hemos iniciado sesión en GMail, la dirección del `src` no devolverá
una imagen, sino que redireccionará a una página HTML. Con los atributos
`onload` y `onerror` podremos distinguir si la imagen ha cargado o no,
por lo que podremos saber si el usuario ha iniciado sesión o no. Esto
parece que funciona en Firefox, Chrome, Opera, Safari y varias versiones
de Internet Explorer.

Parece que si [en Firefox tenemos desmarcada][] la opción de "Aceptar
cookies de terceros", este ataque ya no funciona. Para comprobar el
estado de esta opción vamos al menú Editar > Preferencias > Privacidad
> Usar configuración personalizada para el historial.

Twitter
-------

Conectado a Twitter? __**...**__

En el caso de Twitter, se utiliza una etiqueta `script`, por lo que el
usuario deberá tener el Javascript habilitado para que funcione. En este
caso, el `src` hace referencia a una página sólo visible si el usuario
está conectado. En caso contrario, se produce una redirección. Aquí es
donde entran los diferentes códigos de estado de HTTP. Facebook, Twitter
o Digg proporcionan diferentes código de estado para algunas URLs
dependiendo de si el usuario está conectado o no.

En Firefox, Safari y Chrome, la etiqueta `script` ejecuta el `onload` si
el `src` devuelve un `200 OK`, incluso si el contenido devuelto no es
código Javascript. Si el código es 404, 403, 406 o 500, se ejecuta el
`onerror`.

```
<script type="text/javascript"
        src="https://twitter.com/settings/accounts/update?authenticity_token=xxx"
        onload="logged_in('lit', 'Si')"
        onerror="logged_in('lit', 'No')"
        async="async">

```

```
<script type="text/javascript"
        src="https://twitter.com/settings/accounts/update?authenticity_token=xxx"
        onload="not_logged_in_twitter()"
        onerror="logged_in_twitter()"
        async="async">

```

En este caso, Twitter redirige a la página de _login_ si el usuario no
está conectado, pero devuelve una página de error si el usuario está
conectado, ya que la URL que hemos puesto corresponde a un formulario
que debe ser enviado por `POST` y no por `GET`, además de que no
conocemos el valor del campo `authenticity_token`.

Si Twitter [está bloqueado][] y nos conectamos desde detrás de un proxy,
es posible que el _script_ nos diga que estamos conectados cuando en
realidad no es así.

Facebook
--------

Conectado a Facebook? __**...**__


En el caso de Facebook también recuriremos a una etiqueta `script`, y en
el `src` podemos poner la URL de un perfil que sólo sea visible si el
usuario está conectado, por ejemplo el de Mike.

```
<script type="text/javascript"
        src="https://www.facebook.com/imike3"
        onload="logged_in('lif','Sí')"
        onerror="logged_in('lif','No')"
        async="async">

```

```
<script type="text/javascript"
        src="https://www.facebook.com/imike3"
        onload="logged_in_to_facebook()"
        onerror="not_logged_in_to_facebook()"
        async="async"
>
```
```

En algunas ocasiones, parece que Facebook añade algún tipo de
[comprobación de seguridad][], como añadir un _captcha_, antes de
mostrar el perfil, o el error en caso de no estar conectado, por lo que
el código de esa página previa es un `200 OK`, y mostraría al usuario
conectado cuando en realidad puede no ser así.

En los comentarios del artículo de Mike hacen referencia a un artículo
anterior de [Jeremiah Grossman][]. Utiliza la misma técnica de la
etiqueta `img` sólo que la imagen a la que hace referencia no es una
imagen del perfil, sino una imagen que debía estar accesible una vez
iniciada la sesión. Sin embargo, esa imagen ahora mismo no está
disponible.

Una cosa que me ha llamado la atención es que hay un ejemplo de cómo
podemos crear un ataque más personalizado. Si hay una persona que
sabemos que va a visitar la web, podemos comprobar si ha iniciado sesión
en el panel de administración de Wordpress que sabemos que tiene
instalado en algún dominio concreto:

```

```

```

```

Aunque ya no funciona, ya que esa imagen ya no existe, y el resto de
imágenes utilizadas en el administrador pueden ser visualizadas sin
tener que haber iniciado sesión.

Para protegernos de estos ataques contra nuestra privacidad podemos
utilizar extensiones como [NoScript][] o [RequestPolicy][].

  [Mark Cardwell]: http://grepular.com/Abusing_HTTP_Status_Codes_to_Expose_Private_Information
  [en Firefox tenemos desmarcada]: http://grepular.com/Abusing_HTTP_Status_Codes_to_Expose_Private_Information#comment1117-1-1-1-2
  [está bloqueado]: http://grepular.com/Abusing_HTTP_Status_Codes_to_Expose_Private_Information?reply_to=11113#comment11113
  [comprobación de seguridad]: http://grepular.com/Abusing_HTTP_Status_Codes_to_Expose_Private_Information#comment18
  [Jeremiah Grossman]: http://jeremiahgrossman.blogspot.com/2008/03/login-detection-whose-problem-is-it.html
  [NoScript]: http://addons.mozilla.org/en-us/firefox/addon/noscript/
  [RequestPolicy]: http://addons.mozilla.org/en-us/firefox/addon/requestpolicy/
