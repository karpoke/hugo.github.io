---
title: "POODLE attacks on SSLv3"
date: 2014-11-14T15:24:00+01:00
draft: false
categories: ["micropost"]
tags: []
slug: "poodle-attacks-on-sslv3"
---
> My colleague, Bodo M¶ller, in collaboration with Thai Duong and
> Krzysztof Kotowicz (also Googlers), just posted details about a
> padding oracle attack against CBC-mode ciphers in SSLv3. This attack,
> called POODLE, is similar to the BEAST attack and also allows a
> network attacker to extract the plaintext of targeted parts of an SSL
> connection, usually cookie data. Unlike the BEAST attack, it doesn’t
> require such extensive control of the format of the plaintext and thus
> is more practical. Fundamentally, the design flaw in SSL/TLS that
> allows this is the same as with Lucky13 and Vaudenay’s two attacks:
> SSL got encryption and authentication the wrong way around – it
> authenticates before encrypting.

» Adam Langley | [imperialviolet.org][]

  [imperialviolet.org]: https://www.imperialviolet.org/2014/10/14/poodle.html
