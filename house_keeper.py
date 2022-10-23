#!/usr/bin/env python3

import argparse
import sys
import os
import fnmatch
from pathlib import Path
import pathlib
from shutil import move
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('dir_to_scan', type=str, help='Path to the directory to scan')
group = parser.add_argument_group()
group.add_argument('-c', '--category', help='Process as category')
group.add_argument('-m', '--manual_mode', action='store_true', help='Manual mode')
group.add_argument('--video_dir', help='Video destination directory')
group.add_argument('--books_dir', help='Books destination directory')
group.add_argument('--audio_dir', help='Video destination directory')

args = parser.parse_args()

video_dir = args.video_dir
audio_dir = args.audio_dir
books_dir = args.books_dir
torrent_dir = None

if not video_dir:
     video_dir = Path.home()/'Videos'
if not books_dir:
     books_dir = Path.home()/'Documents/Books'
if not audio_dir:
     audio_dir = Path.home()/'Music'
if not torrent_dir:
     torrent_dir = Path.home()/'Downloads/Torrent'


def video_handler(path):
     dst_filename = os.path.join(video_dir, os.path.basename(path)); 
     move(path, Path(dst_filename), copy_function = shutil.copytree)

def books_handler(path):
     dst_filename = os.path.join(books_dir, os.path.basename(path)); 
     move(path, Path(dst_filename), copy_function = shutil.copytree)

def audio_handler(path):
     dst_filename = os.path.join(audio_dir, os.path.basename(path)); 
     move(path, Path(dst_filename), copy_function = shutil.copytree)

def torrent_handler(path):
     dst_filename = os.path.join(torrent_dir, os.path.basename(path)); 
     move(path, Path(dst_filename), copy_function = shutil.copytree)

rules={ "*.mp3":"audio"}
video_exts=('ts', 'webm', 'mp4', 'avi', 'mkv', 'm4b')
tmp = { '*.{}'.format(rule): 'video' for rule in video_exts }
rules.update(tmp)
books_exts=('fb2', 'epub', 'pdf', 'djvu', 'doc', 'docx')
tmp = { '*.{}'.format(rule): 'books' for rule in books_exts }
rules.update(tmp)
del tmp
rules['*.torrent'] = 'torrent'

handlers={"video": video_handler, "audio": audio_handler, 'books': books_handler, 'torrent': torrent_handler}

def process_dir(folder, level=0):
     def print_indented(folder, level):
        print('\t' * level + (folder))

     #print_indented(Path(folder).name, level)
     for file in Path(folder).iterdir():
        if file.is_dir():
             process_dir(Path(file), level + 1)
        else:
            #print_indented(file.name, level+1)
            for rule in rules.keys():
               if fnmatch.fnmatch(file.name, rule):
                    category = rules[rule]
                    print('\'{}\' is {}'.format(file.name, category))
                    handler = handlers[category]
                    if handler is not None:
                         handler(file)
               # if (file.stat().st_size / 1024 / 1024) > 50:
               #      print('\'{}\' is a big file'.format(file.name))

if not args.manual_mode:
     process_dir(args.dir_to_scan)
elif args.category:
     source_path = Path(args.dir_to_scan)
     if source_path.exists():
          if source_path.is_dir():
               print('Processing the directory {} as "{}" category.'.format(source_path, args.category))
               handler_func = handlers[args.category]
               if handler_func is not None:
                    handler_func(source_path)
          else:
               handler_func = handlers[args.category]
               if handler_func is not None:
                    handler_func(source_path)
