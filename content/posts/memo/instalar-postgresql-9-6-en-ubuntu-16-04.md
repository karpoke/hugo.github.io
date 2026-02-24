---
title: "Instalar Postgresql 9.6 en Ubuntu 16.04"
date: 2016-12-13T19:24:00+01:00
categories: ["memo"]
tags: ["Postgresql", "9.6", "Ubuntu", "Xenial Xerus", "16.04", "apt-key", "apt", "PPA", "sources.list"]
slug: "instalar-postgresql-9-6-en-ubuntu-16-04"
---
La versión de Postgresql que viene en los repositorios de Ubuntu Xenial Xerus
es la 9.5. Si queremos instalar la 9.6, podemos recurrrir al PPA oficial.

Importamos la clave:

```
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc |
sudo apt-key add -
```

Añadimos el PPA:

```
$ echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" |
sudo tee /etc/apt/sources.list.d/postgresql.list
```

Actualizamos e instalamos:

```
$ sudo apt update
$ sudo apt install postgresql-9.6 postgresql-contrib
```

Referencias
-----------

» [linoxide.com][]

  [linoxide.com]: http://linoxide.com/tools/setup-postgresql-access-phppgadmin-ubuntu-16-04/
