#!/usr/bin/python3
import os
import sys

if sys.version_info[0] < 3:
    raise Exception('Must be using Python 3')

import json
import os
from multiprocessing import Pool

IS_JSON = False

if IS_JSON:
    f = open("subscriptions.json","r")
    subs = json.loads(f.read())
else:
    f = open("subscriptions.csv","r")
    subs = [line.split(",") for line in f.read().split("\n")][:-1]

PATH = os.path.dirname(os.path.abspath(__file__))
FILES = os.listdir(PATH)
VTW  = "videos_to_watch.txt"
for n in FILES:
    if n == VTW:
        os.remove(PATH + "/" + VTW)
    elif len(n) == 28 and n[0:2] == "UC":
        os.remove(PATH + "/" + n)

channel_link = "https://www.youtube.com/channel/"

#yt-dlp --skip-download --print-to-file id last10-channel.txt --playlist-end 10 "channel URL"
#start = "yt-dlp --skip-download --print-to-file \"%(upload_date)s/%(creator)s - %(title)s.%(ext)s\" "
start = "yt-dlp --skip-download --print-to-file "
#start = "youtube-dl --skip-download --print-to-file "
middle = " --playlist-end 10 "

def download(sub):
    if IS_JSON:
        id = sub["snippet"]["resourceId"]["channelId"]
        title = sub["snippet"]["title"]
    else:
        id = sub[0]
        title = sub[2]
    curr_channel_link = channel_link + id
    output_format = " \"" + str(title) + "\thttps://www.youtube.com/watch?v=%(id)s\t%(upload_date)s\t%(title)s\" "
    script = start + output_format + id + ".txt" + middle + '\"' + curr_channel_link + '\"'
    stream = os.popen("cd " + PATH + " && " + script)
    print(curr_channel_link)
    print(script)
    print(stream.read())

with Pool(max(os.cpu_count()-2,1)) as p:
    p.map(download,subs)

videos_array = []

for file in os.listdir(PATH):
    if len(file) >= 24 and file[0:2] == "UC":
        curr_file = [n.split("\t") for n in open(file,"r").read().split("\n")][:-1]
        videos_array.extend(curr_file)

videos_array.sort(key=lambda x : -int(x[-2]))

videos_to_watch = open("videos_to_watch.html","w")

output = "<table>"

for n in videos_array:
    output += "<tr>"
    output += "<th>" + n[0] + "</th>"
    output += "<th>" + "<a href=\"" + n[1] + "\">" + n[1] + "</a>" + "</th>"
    output += "<th>" + n[2] + "</th>"
    output += "<th>" + n[3] + "</th>"
    output += "</tr>"

output += "</table>"

videos_to_watch.write(output)
print(output)

'''
TODO:
Filter out shorts
Find out long channel id
'''
