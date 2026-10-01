---
title: "Superfast portscanner"
date: 2021-09-26T20:21:01+01:00
categories: ["micropost"]
tags: []
slug: "superfast-portscanner"
---
> time seq 65535 | parallel -k --joblog portscan -j9 --pipe --cat -j200%
> -n9000 --tagstring

» commandlinefu.com | [commandlinefu.com][]

  [commandlinefu.com]: https://www.commandlinefu.com/commands/view/25535/superfast-portscanner
