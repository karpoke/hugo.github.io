---
title: "Importar un volcado de datos en MySQL"
date: 2011-03-27T22:09:00+01:00
draft: false
categories: ["admin"]
tags: ["mysql", "mysqldump", "mysqlimport"]
slug: "importar-un-volcado-de-datos-en-mysql"
---
Para realizar un volcado de datos, podemos ejecutar:

```
$ mysqldump -uuser -p --all-databases --host localhost > mysql.sql
```

![MySQL Dump]({static}/images/mysqldump.png )

_Fuente: [luauf.com][]_

Para importar este volcado, existe la herramienta `mysqlimport`:

```
$ mysqlimport -uuser -hhost -p --local dbname mysql.sql
```

Sin embargo, no me acaba de ir bien, ya que me devuelve este error:

```
mysqlimport: Error: 1146, Table 'dbname.mysql' doesn't exist, when using table: mysql
```

Una forma de conseguir [restaurar el volcado de datos][] es desde el
cliente de `mysql`:

```
$ mysql -uuser -p dbname
mysql> source mysql.sql;
mysql> exit;
```

[Otra forma][]:

```
$ mysql -uuser -p dbname < mysql.sql
```

  [luauf.com]: http://luauf.com/2008/05/17/mysql-shell-script-backup/
  [restaurar el volcado de datos]: http://forums.mysql.com/read.php?10,269126,269264#msg-269264
  [Otra forma]: http://bookmarks.honewatson.com/2008/05/06/mysqlimport-error-table-databasemydatabase-doesnt-exist/
