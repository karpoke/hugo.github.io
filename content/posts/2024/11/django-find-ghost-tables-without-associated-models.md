---
title: "Django: find ghost tables without associated models"
date: 2024-11-26T12:21:02+01:00
categories: ["micropost"]
tags: ["django", "history"]
slug: "django-find-ghost-tables-without-associated-models"
---
> Heavy refactoring of models can leave a Django project with “ghost
> tables”, which were created for a model that was removed without any
> trace in the migration history. Thankfully, by using some Django
> internals, you can find such tables.

» adamj.eu | [adamj.eu][]

  [adamj.eu]: https://adamj.eu/tech/2024/11/21/django-tables-without-models/
