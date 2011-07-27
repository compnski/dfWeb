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
import time
import struct
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

        df_fd = df.stdout.fileno()
        df_fl = fcntl.fcntl(df_fd, fcntl.F_GETFL)
        fcntl.fcntl(df_fd, fcntl.F_SETFL, df_fl | os.O_NONBLOCK)

        n = 0
        f = open("f.log","w")
        print os.getpid(), sys.stdin.fileno()
        epoll = select.poll()
        STDIN = io.FileIO(name=0, closefd=False)
        epoll.register(STDIN, select.POLLIN)
        epoll.register(df_fd, select.POLLIN)
        try:
            t0 = time.time()
            prevTs = 0
            while True:
                n += 1
                ret = epoll.poll(1000)
                if not ret:
                    os.write(readPipe, outputparser.FLUSH_COMMAND)
                for (sock, event) in ret:
                    if sock == STDIN.fileno():
                        d = STDIN.read()
                        if d != "":
                            df.stdin.write(d)
                    elif sock == df_fd:
                        d = os.read(df_fd, 1000)
                        if len(d) == 0:
                            f.close()
                            print 'CLOSING'
                            return
                        ts = int(time.time() - t0) * 1000
                        if ts != prevTs:
                            ts_pack = struct.pack("I", ts)
                            ts_pack = ts_pack.replace("\x1b", "\x1a") #Can't send the escape char do to how the parser works.
                            print >>sys.stderr, ts, ts_pack
                            f.write("\x1bD%s%s" % (ts_pack, d))
                            prevTs = ts
                        else:
                            f.write(d)
                        os.write(readPipe, d)
        except Exception as e:
            print e
            pass
            f.write(str(e))
        finally:
            print "EXITTT"
            os.write(readPipe, "\d")
            f.close()
            #readPipe.close()
            os.close(readPipe)
            print

if __name__ == "__main__":
    from graphics import *
    fd = sys.stdin.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    appWrapper = AppWrapper("df_linux/df")
    #appWrapper = AppWrapper("telnet towel.blinkenlights.nl")
    outputParserServer = outputparser.OutputParserServer(data.escape_code_map)
    (outPipe, inPipe) = outputParserServer.getPipes()
    outputParserServer.start()
    appWrapper.start(outPipe)

    import termModel

    #def __init__(self, glyphManager, gfxTerm, charGroup):
    glyphManager = GlyphManager()
    glyphManager.loadSprite(GlyphManager.VT220_GLYPH_FILENAME, 10, 8)


    g = GfxTerm()
    group = g.getSpriteGroup()
    gfxCharFactory = GfxCharFactory(glyphManager, g, group)
    t = termModel.Terminal(gfxCharFactory, 25, 80)
    g.setTermModel(t)
    t.setDisplay(g)

    while True:
        print '1',
        cmd = inPipe.recv()
        g.sink()
        print '2',
        if cmd == "QUIT":
            break
        if cmd:
            print '3',
            r = t.render(cmd)
            if r:
                print "[","]"

    print "GOODBYE"
    appWrapper.stop()
    outputParserServer.stop()

