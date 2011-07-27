#!/usr/bin/env python
import time
import struct
import string
import sys
from data import *


class Char(object):
    def __init__(self, char, attrs):
        self.char = char
        self.attrs = attrs
        pass
    def __str__(self):
        if self.char not in string.printable:
            return "\\x%x" % ord(self.char)
        return self.char
    def __repr__(self):
        return str(self)

class Cursor(object):
    def __init__(self, parent):
        self.parent = parent
        self.r = 0
        self.c = 0
        self.maxR = self.parent.r
        self.maxC = self.parent.c
        self.attrs = dict(bgColor = colorMap[7],
                          fgColor = colorMap[0],
                          brightness = 'normal',
                          )

    def printString(self, data):
        "Prints a string to the termbuf, returns a list of coords that were updated"
        ret = []
        r = self.r
        c = self.c
        for char in data:
            ret.append((r, c))
            self.parent.setChar(r, c, self._getNewChar(r, c, char))
            r, c = self._getIncrementedCursorPos(r, c, 1)
        self.r = r
        self.c = c
        return ret


    def _getNewChar(self, r, c, char):
        "Return a new Char() object with the current mode and specified character"
        return self.parent._getNewChar(r, c, char)

    def _getIncrementedCursorPos(self, r, c, num):
        "Given a row, column and number of chars printed, return the new cursor position"
        c += num
        while c >= self.parent.c:
            c -= self.parent.c
            r += 1
        if r  >= self.maxR:
            r = self.maxR - 1
            self.parent.scrollUp(1)
        return r, c

    def setMode(self, mode):
        pass
    def resetMode(self, mode):
        pass
    def setRendition(self, args):
        for attr in args:
            if not attr:
                attr = 0
            attr = int(attr)
            if attr == 0:
                self.attrs = self._defaultAttrs()
            elif attr < 3:
                self.attrs['brightness'] = brightnessMap[attr]
            elif attr < 40:
                self.attrs['fgColor'] = colorMap[attr-30]
            else:
                self.attrs['bgColor'] = colorMap[attr-40]

    def setExpandedMode(self, mode):
        pass
    def resetExpandedMode(self, mode):
        pass

    def _defaultAttrs(self):
        return dict(bgColor=(0, 0, 0), fgColor=(255, 255, 255))


class Terminal(object):

    def render(self, object):
        "Takes either a string or action tuple and renders it"
        if type(object) is str:
            self.printString(object)
        else:
            args = []
            for n in object[1:]:
                args.extend(n.split(";"))
            getattr(self, object[0])(*args)
            return object

    def __init__(self, charFactory, r, c):
        self.r = r
        self.c = c
        self.cursor = Cursor(self)
        self.charFactory = charFactory
        self.t0 = int(time.time() * 100000)

    def delay(self, delaytime):
        "Delay until relative time in seconds since start is less than the passed value"
        delaytime = struct.unpack("I", delaytime)[0]
        resumeTime = self.t0 + delaytime
        while int(time.time() * 100000) < resumeTime:
            pass

    def setDisplay(self, display):
        self.display = display
        self.dirtySet = set()
        self.termBuf = self._initializeBuf(self.r)

    def updateDisplay(self, dirtySet = []):
        if not self.display:
            return
        self.dirtySet.update(dirtySet)
        self.display.updateDisplay(self.dirtySet)
        self.dirtySet = set()

    def accumDirtyChar(self, char):
        self.dirtySet.update(char)

    def _getNewChar(self, r, c, char):
        return self.charFactory.getChar(r, c, char, self.cursor.attrs)

    def getAndClearDirtySet(self):
        d = self.dirtySet
        self.dirtySet = set()
        return d

    def _initializeBuf(self, r):
        return self._blankLines(0, r)

    def setChar(self, r, c, char):
        char_ = self.termBuf[r][c]
        if char_:
            char_.remove(self.charFactory.charGroup)
        self.termBuf[r][c] = char

    def getChar(self, r, c):
        return self.termBuf[r][c]

    def printString(self, string):
        self.accumDirtyChar(self.cursor.printString(string))

    def switchCharset(self, charset):
        pass

    def scrollUp(self, n=1):
        for r in self.termBuf[:n]:
            for c in r:
                c.remove(self.charFactory.charGroup)
        self.termBuf = self.termBuf[n:] + self._blankLines(self.cursor.r+1, n)
        for sprite in self.display.group:
            sprite.rect.move_ip(0, -n * self.charFactory.charHeight)
            sprite.dirty = 1

    def scrollDown(self, n=1):

        self.termBuf = self._blankLines(0, n) + self.termBuf[:-n]
        for sprite in self.display.group:
            sprite.rect.move_ip(0, n * self.charFactory.charHeight)
            sprite.dirty = 1

    def _blankLines(self, start_r, n):
        return [[self._getNewChar(start_r + r, c, ' ') for c in xrange(self.c)] for r in xrange(n)]

    def setRendition(self, *args):
        self.cursor.setRendition(args)

    def setMode(self, *args):
        return "\x1b[%sh" % "".join(args)
    def resetMode(self, *args):
        return "\x1b[%sl" % "".join(args)
    def setExpandedMode(self, *args):
        return "\x1b[?%sh" % "".join(args)
    def resetExpandedMode(self, *args):
        return "\x1b[?%sh" % "".join(args)
    def setKeypad(self, type_='application'):
        if type_ == "application":
            return "\x1b="
        elif type_ == "numeric":
            return "\x1b>"
 
    def scrollRegion(self, r, c):
        return "\x1b[%s;%sr" % (r, c)
    def moveCursor(self, direction, amount='1'):
        amount = int(amount)
        if direction == 'left':
            self.setCursorPos(self.cursor.r, self.cursor.c - amount)
        if direction == 'right':
            self.setCursorPos(self.cursor.r, self.cursor.c + amount)
        if direction == 'down':
            self.setCursorPos(self.cursor.r + amount, self.cursor.c)
        if direction == 'up':
            self.setCursorPos(self.cursor.r - amount, self.cursor.c)

    def setCursorPos(self, r='0', c='0'):
        sep = ";" if r and c else ''
        self.cursor.r = int(r)
        self.cursor.c = int(c)

    def nextLine(self):
        return "\x1bE"

    def saveCursor(self):
        return "\x1b7"
    def restoreCursor(self):
        return "\x1b8"
    def setTabstop(self):
        return "\x1bH"
    def clearTabstop(self):
        return "\x1bg"
    def clearAllTabstop(self):
        return "\x1b3g"
    def reset(self):
        return "\x1bc"
    def fullReset(self):
        return "\x1b[!p"

    def getDevAttributes(self, arg):
        return "\x1b[%sc" % arg
    def getDevStatus(self, arg):
        return "\x1b[%sn" % arg



    def insertLine(self, num=""):
        return "\x1b[%sL" % num
    def deleteLine(self, num=""):
        return "\x1b[%sM" % num
    def insertChar(self, num=""):
        return "\x1b[%s@" % num

    def eraseInScreen(self, args='0'):
        if args == '':
            args = 0
        args = int(args)
        if args == 0:
            self.printString(blankString(self.c - self.cursor.c + ((self.r - self.cursor.r) * self.c)))
        if args == 1:
            curR, curC = self.cursor.r, self.cursor.c
            self.setCursorPos(0, 0)
            self.printString(curC + curR * self.c)
        if args == 2:
            self.charFactory.charGroup.empty()
            self.termBuf = self._initializeBuf(self.r)
            self.setCursorPos(0, 0)

    def eraseInLine(self, args='0'):
        args = int(args)
        if args == 0:
            self.printString(blankString(self.c - self.cursor.c))
        if args == 1:
            oldC = self.cursor.c
            self.cursor.c = 0
            self.printString(blankString(oldC))
        if args == 2:
            self.cursor.c = 0
            self.printString(blankString(self.c))

    def deleteChar(self, num="0"):
        self.eraseChar(num)
    def eraseChar(self, num="0"):
        num = int(num)
        self.printString(blankString(num))


def blankString(num):
    return "".join('' for _ in xrange(num))
