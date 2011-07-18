#!/usr/bin/env python
import sys
import subprocess
import select
import fcntl
from collections import defaultdict
import data
import multiprocessing
import os
import io

import outputparser
import terminalrenderer

class AppWrapper(object):

    def __init__(self, execPath):
        self.execPath = execPath

    def start(self, readPipe, processError=None):
        self.process = multiprocessing.Process(target=self._run, kwargs = {"readPipe":readPipe,
                                                                           "processError":processError})
        self.process.start()
        print >>sys.stderr, "AppWrapper: %d", self.process.pid

    def stop(self):
        self.process.terminate()
        self.process.join()

    def _run(self, readPipe, processError):
        df = subprocess.Popen(self.execPath, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        n = 0
        f = open("f.log","w")
        print os.getpid(), sys.stdin.fileno()
        epoll = select.poll()
        STDIN = io.FileIO(name=0, closefd=False)
        epoll.register(STDIN, select.POLLIN)
        epoll.register(df.stdout, select.POLLIN)
        try:
            while True:
                # df.stdout, 
                n += 1
                #(readReady, _, exceptional) = select.select([sys.stdin], [], [], 5)
                ret = epoll.poll()
                for (sock, event) in ret:
                    if sock == STDIN.fileno():
                        d = STDIN.read()
                        if d != "":
                            f.write(d)
                            df.stdin.write(d)
                    elif sock == df.stdout.fileno():
                        d = df.stdout.read(1)
                        if len(d) == 0:
                            return
                        os.write(readPipe, d)
                        #readPipe.write(d)
        except Exception as e:
            print e
            pass
            #f.write(str(e))
        finally:
            print "EXITTT"
            os.write(readPipe, "\d")
            f.close()
            #readPipe.close()
            os.close(readPipe)
            print

if __name__ == "__main__":
    fd = sys.stdin.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    appWrapper = AppWrapper("df_linux/df")
    outputParserServer = outputparser.OutputParserServer(data.escape_code_map)
    (outPipe, inPipe) = outputParserServer.getPipes()
    outputParserServer.start()
    appWrapper.start(outPipe)

    termEm = terminalrenderer.TerminalRenderer()
    while True:
        cmd = inPipe.recv()
        if cmd == "QUIT":
            break
        if cmd:
            sys.stdout.write(termEm.render(cmd))
    print "GOODBYE"
    appWrapper.stop()
    outputParserServer.stop()
    termEm.log.close()
