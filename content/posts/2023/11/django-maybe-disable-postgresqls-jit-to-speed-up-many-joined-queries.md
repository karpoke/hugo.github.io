---
title: "Django: Maybe disable PostgreSQL’s JIT to speed up many-joined queries"
date: 2023-11-09T23:27:34+01:00
categories: ["micropost"]
tags: ["django", "postgresql", "optimization"]
slug: "django-maybe-disable-postgresqls-jit-to-speed-up-many-joined-queries"
---
> Here’s a write-up of an optimization I made in my client Silvr’s
> project. I ended up disabling a PostgreSQL feature called the JIT
> (Just-In-Time) compiler which was taking a long time for little benefit.

» adamj.eu | [adamj.eu][]

  [adamj.eu]: https://adamj.eu/tech/2023/11/09/django-disable-postgresql-jit/
