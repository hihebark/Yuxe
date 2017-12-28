[![Build Status](https://travis-ci.org/hihebark/Yuxe.svg?branch=master)](https://travis-ci.org/hihebark/Yuxe)

Yuxe
====


Description:
------------

Extract music from compilation, music mix on Youtube, 
Why download one music file whene you can dowload them all separately.

Requirement:
------------

Only youtube_dl you can install it with:

    pip3 install youtube_dl

and you need to for the `ffmpeg`:

    chmod +x yuxe.py

Usage:
------

`python3 yuxe.py -y https://www.youtube.com/watch?v=VIDEO_ID -t tlist.txt -sl ' - '`

    .----.
  t(.___.t) - Yuxe
    `----
  usage: yuxe.py [-h] -ylink YLINK -t-list T_LIST [-split-list SPLIT_LIST]

  Yuxe - Extract music from compilation, music mix on youtube

  optional arguments:
    -h, --help            show this help message and exit
    -ylink YLINK, -y YLINK
                          Link to the youtube video
    -t-list T_LIST, -t T_LIST
                          Track List
    -split-list SPLIT_LIST, -sl SPLIT_LIST
                          the char between the time and the name of the song

