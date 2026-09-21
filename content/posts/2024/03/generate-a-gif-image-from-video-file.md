---
title: "Generate a GIF image from video file"
date: 2024-03-20T10:10:07+01:00
categories: ["micropost"]
tags: []
slug: "generate-a-gif-image-from-video-file"
---
> ffmpeg -ss 30 -t 3 -i input.mp4 -vf
> \"fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\"
> -loop 0 output.gif - (Generate a GIF image from video file The 30 means
> start extracting frames from 30 seconds into the video. The 3 means
> extract the…

» commandlinefu.com | [commandlinefu.com][]

  [commandlinefu.com]: https://www.commandlinefu.com/commands/view/34946/generate-a-gif-image-from-video-file
