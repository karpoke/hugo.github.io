---
title: "Secure Secure Shell"
date: 2015-01-06T19:09:00+01:00
draft: false
categories: ["micropost"]
tags: []
slug: "secure-secure-shell"
---
> Reading the documents, I have the feeling that the NSA can 1) decrypt
> weak crypto and 2) steal keys. Let’s focus on the crypto first. SSH
> supports different key exchange algorithms, ciphers and message
> authentication codes. The server and the client choose a set of
> algorithms supported by both, then proceed with the key exchange. Some
> of the supported algorithms are not so great and should be disabled
> completely. If you leave them enabled but prefer secure algorithms,
> then a man in the middle might downgrade you to bad ones. This hurts
> interoperability but everyone uses OpenSSH anyway.

» [stribika.github.io][]

  [stribika.github.io]: https://stribika.github.io/2015/01/04/secure-secure-shell.html
