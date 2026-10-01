---
title: "Download screenshot or frame from YouTube video at certain timestamp"
date: 2021-07-06T19:10:06+01:00
categories: ["micropost"]
tags: []
slug: "download-screenshot-or-frame-from-youtube-video-at-certain-timestamp"
---
> ffmpeg -ss 8:14 -i $(youtube-dl -f 299 --get-url URL) -vframes 1 -q:v 2
> out.jpg - (Download screenshot or frame from YouTube video at certain
> timestamp Downloads the frame of given YouTube video at 8 minutes 14
> seconds. Requested format is \"299\", which 1080p only video.). The…

» commandlinefu.com | [commandlinefu.com][]

  [commandlinefu.com]: https://www.commandlinefu.com/commands/view/25399/download-screenshot-or-frame-from-youtube-video-at-certain-timestamp
