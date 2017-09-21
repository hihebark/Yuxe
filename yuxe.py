#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from libs.mLogger import MyLogger
import os, sys
import subprocess
import time

if sys.version[0] == '2':
    print("Required Python 3")
    exit(1)

try:
    import youtube_dl
except:
    print('''[e] install youtube_dl: pip install -U youtube_dl. or pip3 install youtube_dl''')
    exit(1)

BANNER = "\033[92mt(.___.t) - Yuxe\033[0m"

def my_hook(d):
    if d['status'] == 'finished':
        print("[!] Done downloading.")
    if d['status'] == 'downloading':
        print('\rDownloading {} | Estimation: {}'.format(d['_percent_str'], d['_eta_str']), end='', flush=True)

def makeFile(mName):
    try:
        os.makedirs(mName)
    except IOError as e:
        pass

def getInfo(vlink, ydl_opts = {'logger': MyLogger()}):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_title = ydl.extract_info(vlink, download=False).get('title', None)
        video_lenght = ydl.extract_info(vlink, download=False).get('duration', None)
    return video_title, video_lenght

def downloadVideo(vlink):
    ydl_opts = {
    'outtmpl': 'tmp/test.mp3',
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
    parser = argparse.ArgumentParser(description="Yuxe - Extract music from compilation, music mix on Youtube")
    parser.add_argument("-ylink", help="Link to the youtube video")
    parser.add_argument('-t-list', help="Track List")
    args = parser.parse_args()
    vlink = args.ylink
    t_list = args.t_list
    vName, vLenght = getInfo(vlink)
    vLenght = time.strftime('%H:%M:%S', time.gmtime(vLenght))
    print("Video name: \033[91m{}\033[0m Lenght: \033[91m{}\033[0m".format(vName, vLenght))
    makeFile(vName)
    downloadVideo(vlink)
    print('[!]Reading track list ...')
    m_input = 'tmp/test.mp3'
    for i in range(sum(1 for line in open(t_list))):
        print("[*]Extracting: {}".format(getLineList(t_list, i).split(' ', 1)[1]))
        m_start = getLineList(t_list, i).split(' ', 1)[0]
        m_toend = vLenght if i+1 == sum(1 for line in open(t_list)) else getLineList(t_list, i+1).split(' ', 1)[0]
        m_output = vName+'/'+getLineList(t_list, i).split(' ', 1)[1]+'.mp3'
        subprocess.call(["ffmpeg -hide_banner -loglevel panic -ss {0} -t {1} -i {2} '{3}'".format(m_start, m_toend, m_input, m_output)], shell=True)

if __name__ == '__main__':
    print(BANNER)
    main()
    
    
    
    
    
    
    
    
