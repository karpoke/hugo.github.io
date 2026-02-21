---
title: "SWI-Prolog conoce el sentido de la vida, del universo y de todo lo demas"
date: 2011-01-18T12:22:00+01:00
draft: false
categories: ["memo"]
tags: ["42", "el sentido de la vida", "swi-prolog", "swipl"]
slug: "swi-prolog-conoce-el-sentido-de-la-vida-del-universo-y-de-todo-lo-demas"
---
Ejecutamos `swipl`, uno de los compiladores de Prolog libres:

```
$ swipl
```

![Marvin](/images/marvin-186x300.jpg)

Y si le interrogamos por el valor de una variable de la cual no puede
inferir ningún valor...

```
% library(swi_hooks) compiled into pce_swi_hooks 0.00 sec, 2,060 bytes
Welcome to SWI-Prolog (Multi-threaded, 32 bits, Version 5.8.2)
Copyright (c) 1990-2009 University of Amsterdam.
SWI-Prolog comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions.
Please visit http://www.swi-prolog.org for details.
```

```
For help, use ?- help(Topic). or ?- apropos(Word).
```

```
?- K.
% ... 1,000,000 ............ 10,000,000 years later
%
%       >> 42 << (last release gives the question)
```
