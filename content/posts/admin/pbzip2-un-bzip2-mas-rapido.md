---
title: "pbzip2, un bzip2 más rápido"
date: 2012-06-13T18:43:00+01:00
draft: false
categories: ["admin"]
tags: ["bzip2", "compresión de archivos", "pbzip2"]
slug: "pbzip2-un-bzip2-mas-rapido"
---
`pbzip2`, de _parallel bzip2_, permite aprovechar toda la potencia de
los procesadores con más de un núcleo a la hora de comprimir o
descomprimir, cosa que `bzip2` no hace.

Instalación
-----------

En Ubuntu se encuentra disponible en los repositorios:

```
$ sudo aptitude install pbzip2
```

Su uso es idéntico al de `bzip2`, por lo que podemos añadir un _alias_ a
`~/.bash_aliases`:

```
alias bzip2=pbzip2
```

Referencias
-----------

» [Speed Up Compression via Parallel BZIP2 (PBZIP2)][]

  [Speed Up Compression via Parallel BZIP2 (PBZIP2)]: http://hackercodex.com/guide/parallel-bzip-compression/
