---
title: "Mystery"
date: 2011-02-26T00:49:00+01:00
draft: false
categories: ["dev"]
tags: ["generador", "list comprehension", "python", "yield"]
slug: "mystery"
---
Casi parece que está escrito en chino, o mejor dicho en _brainfuck_, o
puede que no sea muy _[zen]_, pero no deja de ser _[elegante]_.

```
def mystery(n):
    a = list(range(n))
    [[(yield i) for a[::i] in [([0]*n)[::i]]] for i in a[2:] if a[i]]
```

El nombre de la función pretende no dar pistas para que intentemos
averiguar qué hace exactamente esta función. He aquí una pista:

![prime numnbers](/images/prime-numbers-300x300.gif "prime-numbers")

Fuente: [numberspiral.com]

```
>>> f = mystery(20)
>>> try:
...     while True:
...         print f.next()
... except StopIteration:
...     pass
2
3
5
7
11
13
17
19
```

  [zen]: {{< relref "/posts/dev/python-zen.md" >}}
  [elegante]: http://blog.garlicsim.org/post/3504711416#comment-156082460
  [numberspiral.com]: http://www.numberspiral.com/
