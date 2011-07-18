
class TerminalRenderer(object):

    def __init__(self):
        pass

    def render(self, object):
        "Takes either a string or action tuple and renders it"
        if type(object) is str:
            return self.printString(object)
        else:
            return getattr(self, object[0])(*object[1:])

    def printString(self, string):
        return string

    def switchCharset(self, charset):
        if charset == "UK-g0":
            return "\x1b(A"
        elif charset == "UK-g1":
            return "\x1b)A"
        elif charset == "ASCII-g0":
            return "\x1b(B"
        elif charset == "ASCII-g1":
            return "\x1b)B"
        elif charset == "ASCII-g2":
            return "\x1b*B"
        elif charset == "ASCII-g3":
            return "\x1b+B"
        elif charset == "DEC-g0":
            return "\x1b(0"
        elif charset == "DEC-g1":
            return "\x1b)0"

    def setRendition(self, *args):
        return "\x1b[%sm" % "".join(args)
    def setMode(self, *args):
        return "\x1b[%sh" % "".join(args)
    def resetMode(self, *args):
        return "\x1b[%sl" % "".join(args)
    def setExpandedMode(self, *args):
        return "\x1b[?%sh" % "".join(args)
    def resetExpandedMode(self, *args):
        return "\x1b[?%sh" % "".join(args)
    def setKeypad(self, type_):
        if type_ == "application":
            return "\x1b="
        elif type_ == "numeric":
            return "\x1b>"
    def scrollRegion(self, r, c):
        return "\x1b[%s;%sr" % (r, c)
    def moveCursor(self, direction, amount=''):
        dir_map  = {"up":"A",
                    "down":"B",
                    "left":"C",
                    "right":"D"}
        return "\x1b[%s%s" % (amount, dir_map[direction])
    def setCursorPos(self, r='', c=''):
        sep = ";" if r and c else ''
        return "\x1b[%s%s%sH" % (r, sep, c)
    def index(self):
        return "\x1bD"
    def reverseIndex(self):
        return "\x1bM"
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
    def eraseInLine(self, args=''):
        return "\x1b[%sK" % args
    def eraseInScreen(self, args=''):
        return "\x1b[%sJ" % args

    def getDevAttributes(self, arg):
        return "\x1b[%sc" % arg
    def getDevStatus(self, arg):
        return "\x1b[%sn" % arg

    def deleteChar(self, num=""):
        return "\x1b[%sP" % num
    def insertLine(self, num=""):
        return "\x1b[%sL" % num
    def deleteLine(self, num=""):
        return "\x1b[%sM" % num
    def insertChar(self, num=""):
        return "\x1b[%s@" % num
    def eraseChar(self, num=""):
        return "\x1b[%sX" % num

