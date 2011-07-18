#!/usr/bin/env python
import sys
import subprocess
import select
import fcntl
from collections import defaultdict
import data
import multiprocessing

import inputparser
import terminalrenderer

class AppWrapper(object):

    def __init__(self, execPath, dataCallback):
        self.execPath = execPath
        self.dataCallback = dataCallback
        self.df = subprocess.Popen(self.execPath, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def start(self, processRead, processError=None):
        self.process = multiprocessing.Process(target=self._run, kwargs{"processRead":processRead,
                                                                        "processError":processError})

    def _run(self, processRead, processError):
        while True:
            (readReady, _, exceptional) = select.select([df.stdout], [], [df.stdout], 5)
            for sock in exceptional:
                print "Error with a socket: ", sock
            for sock in readReady:
                processRead(sock.read(1))

if __name__ == "__main__":
    appWrapper = AppWrapper("df_linux/df")
    inputParserServer = inputparser.InputParserServer(data.escape_code_map)
    (outPipe, inPipe) = inputParserServer.getPipes()
    inputParserServer.start()
    appWrapper.start(outPipe.send)

    termEm = terminalrenderer.TerminalRenderer()
    while True:
        cmd = inPipe.recv()
        print termEm.render(cmd)
