---
title: "Disk usage skipping mount points (even top-level ones)"
date: 2024-02-28T08:48:26+01:00
categories: ["micropost"]
tags: []
slug: "disk-usage-skipping-mount-points-even-top-level-ones"
---
> for a in /*; do mountpoint -q -- \"$a\" || du -shx \"$a\"; done | sort
> -h - (Disk usage skipping mount points (even top-level ones) Other
> solutions that involve doing $ du -sx /* are incomplete because they
> will still descend other top-level filesystems are that mounted…

» commandlinefu.com | [commandlinefu.com][]

  [commandlinefu.com]: https://www.commandlinefu.com/commands/view/34690/disk-usage-skipping-mount-points-even-top-level-ones
