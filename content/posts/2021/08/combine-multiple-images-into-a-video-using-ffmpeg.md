---
title: "Combine multiple images into a video using ffmpeg"
date: 2021-08-01T13:28:20+01:00
categories: ["micropost"]
tags: []
slug: "combine-multiple-images-into-a-video-using-ffmpeg"
---
> ffmpeg -start_number 0053 -r 1/5 -i IMG_%04d.JPG -c:v libx264 -vf fps=25
> -pix_fmt yuv420p out.mp4 - (Combine multiple images into a video using
> ffmpeg The -start_number can be ignored if sequence starts with 0,
> otherwise use first number in sequence). The best command line…

» commandlinefu.com | [commandlinefu.com][]

  [commandlinefu.com]: https://www.commandlinefu.com/commands/view/25460/combine-multiple-images-into-a-video-using-ffmpeg
