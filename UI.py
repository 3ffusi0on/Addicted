#!/usr/bin/env python3.4
import sys
from PyQt4 import QtGui
import re
import os, sys
import subprocess
import urllib.request
import urllib.error
import hashlib

#TODO
#-input for the link of xdcc server
#-dl button ? or automatize the action
#- /!\ Configuration file /!\
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

class UI(QtGui.QWidget):

    def __init__(self):
        super(UI, self).__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, 300, 120)
        self.setWindowTitle('Addict7ed-to-Xdcc')

        self.link = QtGui.QLineEdit()
        #TODO make it like a promt
        self.link.setText("Xdcc link...")

        #xdcc file download button
        downloadMovieButton = QtGui.QPushButton('Get movie')
        downloadMovieButton.resize(downloadMovieButton.sizeHint())
        downloadMovieButton.clicked.connect(self.downloadXdccFile)

        #pick file button
        pickButton = QtGui.QPushButton('Open...')
        pickButton.resize(pickButton.sizeHint())
        pickButton.clicked.connect(self.selectFile)

        #selected file
        self.filename = QtGui.QLabel()
        self.filename.setText("...")

        #subtitle download button
        downloadSubButton = QtGui.QPushButton('Get Subtitle')
        downloadSubButton.resize(downloadSubButton.sizeHint())
        downloadSubButton.clicked.connect(self.downloadSubtitle)

        ## Layouts
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.link)
        vbox.addWidget(downloadMovieButton)
        vbox.addWidget(pickButton)
        vbox.addWidget(self.filename)
        vbox.addWidget(downloadSubButton)

        self.setLayout(vbox)
        self.show()

    def selectFile(self):
        self.filename.setText(QtGui.QFileDialog.getOpenFileName())
        print(self.filename.text())

    def downloadXdccFile(self):
        print("TODO")

    def downloadSubtitle(self):
        filename = self.filename.text()
        track_hash = get_hash(filename)
        headers = { 'User-Agent' : 'SubDB/1.0 (Addict7ed-to-Xdcc/1.0; http://github.com/3ffusi0on/Addict7ed-to-Xdcc)' }
        url = "http://api.thesubdb.com/?action=download&hash=" + track_hash + "&language=en"
        try:
            request = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(request).read()
            print(response)

            #Saving the subtitle fileo
            dest_file = filename.replace(filename[-3:], 'srt')
            print("Saving subtitle as :" + dest_file)
            subtitle_file = open(dest_file, 'wb')
            subtitle_file.write(response)
            subtitle_file.close()
        except urllib.error.HTTPError as e:
            #TODO check error (missing subtitle on server)
            if e.code == 404:
                print("404 Not Found: No subtitle available for the movie")



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = UI()

    sys.exit(app.exec_())
