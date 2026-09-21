---
title: "Django: model field choices that can change without a database migration"
date: 2025-05-04T08:29:09+01:00
categories: ["micropost"]
tags: ["django", "database"]
slug: "django-model-field-choices-that-can-change-without-a-database-migration"
---
> Adam Hill posted a question on Mastodon: he wants a model field that
> uses choices that doesn’t generate a database migration when the choices
> change. This post presents my answer. First, we’ll recap Django’s
> default behaviour with choice fields, a solution with callable choices…

» adamj.eu | [adamj.eu][]

  [adamj.eu]: https://adamj.eu/tech/2025/05/03/django-choices-change-without-migration/
