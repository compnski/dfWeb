import sys
import os
import time
import termios
import fcntl
import struct
import array
import select

#master = os.open("/dev/ptmx", os.O_RDRW | O_NOCTTY)

class Error(BaseException): pass

def forkpty(attrs=[], winsz=[]):
    (master, slave) = os.openpty()
    if attrs:
        termios.tcsetattr(slave, termios.TCSADRAIN, attrs)
    if winsz:
        if len(winsz) not in (2,4):
            raise TypeError("winsz must be a 2-element array")
        winsz[2],winsz[3] = 0,0
        fcntl.ioctl(slave, termios.TIOCSWINSZ, winsz)

    pid = os.fork()
    if pid:
        os.close(slave)
        return (pid, master)
    else:
        os.close(master)
        os.setsid()
        if fcntl.ioctl(slave, termios.TIOCSCTTY):
            raise Error("failed to ioctl TIOCSCTTY")
        os.dup2(slave, 0)
        os.dup2(slave, 1)
        #os.dup2(slave, 2)
        if slave > 2:
            os.close(slave)
        return (0, 0)




def poll(termFd):
    readable, _, exceptional = select.select([termFd], [], [], 0)
    #print readable, exceptional
    return readable


def runMaster(childPid, masterTerm):
    print 'lsof -p %d' % os.getpid()
    time.sleep(3)
    while poll(masterTerm):
        buf = os.read(masterTerm, 1000)
        if len(buf) == 0:
            return
    pass

def runSlave(path, args, env):
    env["DYLD_FALLBACK_LIBRARY_PATH"]='./libs/'
    env["DYLD_FALLBACK_FRAMEWORK_PATH"]='./libs/'
    env["TERM"] = "vt220"
    os.execve(path, args, env)

buf = array.array('h', [0,0,0,0])
z = fcntl.ioctl(1, termios.TIOCGWINSZ, buf, True)
winsz = buf
print winsz

attrs = termios.tcgetattr(0)

(pid, term) = forkpty(attrs, winsz)

if pid:
    runMaster(pid, term)
else:
    os.chdir("df_osx")
    path = "./dwarfort.exe"
    args = ["/./dwarfort.exe"]
    runSlave(path, args, os.environ)
