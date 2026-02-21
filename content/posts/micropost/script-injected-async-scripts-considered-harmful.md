---
title: "Script-injected ”async scripts” considered harmful"
date: 2014-05-23T21:21:00+01:00
draft: false
categories: ["micropost"]
tags: []
slug: "script-injected-async-scripts-considered-harmful"
---
> The inline JavaScript solution has a subtle, but very important (and
> an often overlooked) performance gotcha: inline scripts block on CSSOM
> before they are executed. Why? The browser does not know what the
> inline block is planning to do in the script it is about to execute,
> and because JavaScript can access and manipulate the CSSOM, it blocks
> and waits until the CSS is downloaded, parsed, and the CSSOM is
> constructed and available.

» Ilya Grigorik | [Script-injected "async scripts" considered harmful][]

  [Script-injected "async scripts" considered harmful]: https://www.igvita.com/2014/05/20/script-injected-async-scripts-considered-harmful/
```
"Script-injected "async scripts" considered harmful"
```
