---
title: "The 8085’s register file reverse engineered"
date: 2013-03-31T20:28:00+01:00
categories: ["micropost"]
tags: []
slug: "the-8085s-register-file-reverse-engineered"
---
> On the surface, a microprocessor’s registers seem like simple storage,
> but not in the 8085 microprocessor. Reverse-engineering the 8085
> reveals many interesting tricks that make the registers fast and
> compact. The picture below shows that the registers and associated
> control circuitry occupy a large fraction of the chip, so efficiency
> is important. Each bit is implemented with a surprisingly compact
> circuit. The instruction set is designed to make register accesses
> efficient. An indirection trick allows quick register exchanges. Many
> register operations use the unexpected but efficient data path of
> going through the ALU.

» Ken Shirriff | [righto.com][]

  [righto.com]: http://www.righto.com/2013/03/register-file-8085.html
