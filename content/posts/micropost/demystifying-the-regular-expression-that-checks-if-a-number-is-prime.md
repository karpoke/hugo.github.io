---
title: "Demystifying the regular expression that checks if a number is prime"
date: 2016-09-10T18:02:00+01:00
draft: false
categories: ["micropost"]
tags: []
slug: "demystifying-the-regular-expression-that-checks-if-a-number-is-prime"
---
> A while back I was researching the most efficient way to check if a number
> is prime. This lead me to find the following piece of code:
>
>     public static boolean isPrime(int n) {
>         return !new String(new char[n]).matches(”.?|(..+?)\\1+”);
>     }
>
> I was intrigued. While this might not be the most efficient way, it’s
> certainly one of the less obvious ones, so my curiosity kicked in. How on
> Earth could a match for the .?|(..+?)\1+ regular expression tell that a
> number is not prime (once it’s converted to its unary representation)?

» iluxonchik | [iluxonchik.github.io][]

  [iluxonchik.github.io]: https://iluxonchik.github.io/regular-expression-check-if-number-is-prime/
