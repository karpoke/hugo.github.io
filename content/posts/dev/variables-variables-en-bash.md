---
title: "Variables variables en Bash"
date: 2011-06-29T12:11:00+01:00
draft: false
categories: ["dev"]
tags: ["bash", "eval", "ksh", "php", "shell", "variables"]
slug: "variables-variables-en-bash"
---
Las variables variables se utilizan cuando queremos tener nombres de
variables que puedan usarse y modificarse de forma dinámica. [PHP
permite su uso][] de forma directa:

```
<?php
$a = 'hello';
?>
```

Una variable variable toma el valor de una variable y lo usa para el
nombre de la variable. Podemos utilizar "hello" como nombre de variable
utilizando dos signos de dólar:

```
<?php
$$a = 'world';
?>
```

En este punto tenemos dos variables, `$a` que contiene "hello" y
`$hello` que contiene "world". Así, las siguientes instrucciones
escriben "hello world":

```
<?php
echo "$a ${$a}";
echo "$a $hello";
?>
```

En Bash
-------

También podemos conseguir [variables variables en Bash][]:

```
$ a=hello
$ b=a
$ echo $a ${!b}
hello hello
```

Algunos tipos de _shell_, como `ksh`, no aceptan la sintaxis anterior,
pero podemos recurrir a `eval` para conseguir el mismo resultado:

```
$ a=hello
$ b=a
$ eval echo $a \$$b
hello hello
```

De la misma forma que en el ejemplo en PHP, podemos declarar la variable
variable al tiempo que se asignamos un valor:

```
$ a=hello
$ eval $a=world
$ eval echo $a \$$a
hello world
```

  [PHP permite su uso]: http://php.net/manual/en/language.variables.variable.php
  [variables variables en Bash]: http://www.nickcoleman.org/blog/index.cgi/varindirect!201106291026!unix/
