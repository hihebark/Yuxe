#!/usr/bin/env python3

# -*- coding: utf-8 -*-

#Copyleft 2017 Hihebark
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#( Copyleft license ) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import argparse
from libs.mLogger import MyLogger
import os, sys
import subprocess
import time
from datetime import datetime

if sys.version[0] == '2':
    print("[e] Required Python 3")
    exit(1)

try:
    import youtube_dl
except:
    print('[e] install youtube_dl')
    exit(1)

BANNER = """\033[92m  .----.
t(.___.t) - Yuxe
  `----\033[0m"""

FMT = '%H:%M:%S'

def my_hook(d):
    if d['status'] == 'finished':
        print("\n[!] Done downloading.")
    if d['status'] == 'downloading':
        print('\rDownloading {} | Estimation: {}'
            .format(d['_percent_str'], d['_eta_str']), end='', flush=True)

def makeFile(mName):
    try:
        os.makedirs(mName)
    except IOError as e:
        print(e)

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def getInfo(vlink, ydl_opts = {'logger': MyLogger()}):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_title = ydl.extract_info(vlink, download=False).get('title', None)
        video_lenght = ydl.extract_info(vlink, download=False).get('duration', None)
    return video_title, video_lenght

def downloadVideo(vlink):
    ydl_opts = {
    'outtmpl': 'tmp/tmpfile.mp3',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vlink])

def getLineList(t_list, m_line_nbr):
    return (open(t_list).readlines()[m_line_nbr]).rstrip('\n')

def main():

    parser  = argparse.ArgumentParser(description="Yuxe - Extract music from compilation, music mix on Youtube")
    parser.add_argument('-ylink', '-y', help="Link to the youtube video", required=True)
    parser.add_argument('-t-list', '-t', help="Track List", required=True)
    parser.add_argument('-split-list', '-sl', help="the char between the time and the name of the song")

    args        = parser.parse_args()
    vlink       = args.ylink
    t_list      = args.t_list
    split_list  = " " if args.split_list is None else args.split_list

    vName, vLenght = getInfo(vlink)
    vLenght = time.strftime(FMT, time.gmtime(vLenght))

    print("Video name: \033[91m{}\033[0m Lenght: \033[91m{}\033[0m".format(vName, vLenght))

    downloadVideo(vlink)
    makeFile(vName)

    print('[!] Reading track list ...')
    m_input = 'tmp/tmpfile.mp3'
    #https://stackoverflow.com/questions/37886305/datetime-get-the-hour-in-2-digit-format
    for mLine in range(sum(1 for line in open(t_list))):

        m_start_track = getLineList(t_list, mLine).split(split_list, 1)[0]
        if (mLine+1) < sum(1 for line in open(t_list)):
            m_duration_track = datetime.strptime(getLineList(t_list, mLine+1).split(split_list, 1)[0], FMT) - datetime.strptime(m_start_track, FMT)
        else:
            m_duration_track = datetime.strptime(vLenght, FMT) - datetime.strptime(m_start_track, FMT)
        m_output = vName+'/'+getLineList(t_list, mLine).split(split_list, 1)[1]+'.mp3'
        print("[*] Extracting: {0} duration: {1}"
            .format(getLineList(t_list, mLine).split(split_list, 1)[1], m_duration_track))
        subprocess.call(["ffmpeg -hide_banner -loglevel fatal -ss {0} -t {1} -i {2} {3}"
            .format(m_start_track, m_duration_track, shellquote(m_input), shellquote(m_output))], shell=True)
    os.system("rm -f tmp/tmpfile.mp3")
if __name__ == '__main__':
    print(BANNER)
    main()
