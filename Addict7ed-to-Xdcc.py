#!/usr/bin/env python2

import re
import os, sys
import subprocess
import urllib2
import hashlib

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

if len(sys.argv) < 3:
    sys.exit('Usage: %s <bot_name> <file_number> [<channel_name>]' % sys.argv[0])

bot_name = sys.argv[1]
file_number = sys.argv[2]
if len(sys.argv) == 4:
    channel_name = sys.argv[3]
else:
    channel_name = ""
server = ""

##Downloading from dcc server
print("Downloading file '" + file_number + "' from bot '" + bot_name + "'")
output = subprocess.Popen(["ruby", "-W0", "./RubyXDCCGetter/xdcc.rb", server, bot_name, file_number,
                "-c", channel_name],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

##mp4 track file
track_file = re.findall('File: (.*?)\*Size', output)[0]# + "mp4" #TODO ugly workaround to fix

##Subtitle file
print("Downloading subtitle for track : " + track_file)
track_hash = get_hash(track_file)
headers = { 'User-Agent' : 'SubDB/1.0 (Addict7ed-to-Xdcc/1.0; http://github.com/3ffusi0on/Addict7ed-to-Xdcc)' }
url = "http://api.thesubdb.com/?action=download&hash=" + track_hash + "&language=en"
request = urllib2.Request(url, '', headers)
response = urllib2.urlopen(request).read()

#Saving the subtitle file
dest_file = track_file.replace('mp4', 'srt')
print("Saving subtitle as :" + dest_file)
subtitle_file = open(dest_file, 'w')
subtitle_file.write(response)
subtitle_file.close()
