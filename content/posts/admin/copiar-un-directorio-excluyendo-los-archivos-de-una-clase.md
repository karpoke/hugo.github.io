---
title: "Copiar un directorio excluyendo los archivos de una clase"
date: 2011-05-11T21:09:00+01:00
draft: false
categories: ["admin"]
tags: ["dropbox", "rsync", "svn"]
slug: "copiar-un-directorio-excluyendo-los-archivos-de-una-clase"
---
Si queremos copiar un directorio pero no queremos que se copien los
archivos `.svn`, o `.dropbox`, podemos ejecutar:

```
$ rsync -r --exclude=.dropbox /path/source/dir /path/destination
```
