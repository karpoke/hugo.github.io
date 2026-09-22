---
title: "Get the beats per minute from an audio track"
date: 2023-09-17T20:21:27+01:00
categories: ["micropost"]
tags: []
slug: "get-the-beats-per-minute-from-an-audio-track"
---
> ffmpeg -loglevel quiet -i \"$AUDIO_FILE\" -f f32le -ac 1 -ar 44100 - |
> bpm - (Get the beats per minute from an audio track Requires bpm-tools
> https://www.pogo.org.uk/~mark/bpm-tools/). The best command line
> collection on the internet, submit yours and save your favorites.

» commandlinefu.com | [commandlinefu.com][]

  [commandlinefu.com]: https://www.commandlinefu.com/commands/view/32816/get-the-beats-per-minute-from-an-audio-track
