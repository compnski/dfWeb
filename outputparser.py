import re
from collections import defaultdict

import multiprocessing
class InputParserServer(object):

    def __init__(self, escape_code_map):
        self.inputParser = InputParser()
        self.inputParser.loadEscapeMap(escape_code_map)
        (self.charPipe, self.commandPipe) = multiprocessing.Pipe(True)


    def getPipes(self):
        "Returns a tuple of outPipe, inPipe. Caller writes to outPipe, reads from inPipe"
        return self.charPipe, self.commandPipe

    def start(self):
        self.process = multiprocessing.Process(target=self._run, name="InputParserServer")
        self.process.start()

    def stop(self):
        self.charPipe.close()
        self.commandPipe.close()
        self.process.join()

    def _run(self):
        try:
            while True:
                char = self.charPipe.recv():
                ret = self.inputParser.parseChar(char)
                if ret is not None:
                    self.commandPipe.put(ret[0])
                    self.commandPipe.put(ret[1])
        except EOFError:
            return

class InputParser(object):

    MAX_SEQUENCE = 20
    def __init__(self):
        self.regexList = []
        self.buf = []

    def addEscapeCode(self, key, meaningTuple):
        regex = self.escapeCodeToRegex(key)
        regex = r"^%s([^\x1b]*)$" % regex
        print regex
        pattern = re.compile(regex)
        self.regexList.append((pattern, meaningTuple))

        self.seqLen = 0
        self.maxSeqLen = 0
        self.maxBuf = ""

        self.undecodedMap = defaultdict(int)

    def parseChar(self, char):
        if char is None:
            b = self.buf
            self.buf = []
            return self.match("".join(b))

        self.seqLen += 1
        if self.buf and (char == "\x1b" or self.seqLen > InputParser.MAX_SEQUENCE):
            b = self.buf
            self.buf = [char]
            if b[0] != "\x1b":
                self.seqLen = 0
                return "".join(b)
            match = self.match("".join(b))
            self.logStats(match)
            return match
        self.buf.append(char)

    def logStats(self, match):
        self.seqLen -= len(match[1]) #subtract non-sequence chars
        self.maxSeqLen = max(self.seqLen, self.maxSeqLen)
        if self.maxSeqLen == self.seqLen:
            self.maxBuf = b
        self.seqLen = 0
        if type(match) == str and match[0] == "\x1b":
            self.logUndecoded(str)
        return match

    def match(self, buf):
        for (pattern, actionTuple) in self.regexList:
            matcher = pattern.match(buf)
            if matcher is not None:
                #print matcher.groups()
                return (actionTuple + tuple(matcher.groups()[:-1]), matcher.groups()[-1])
        return buf, ""

    def logUndecoded(self, buf):
        self.undecodedMap[buf] += 1

    def escapeCodeToRegex(self, code):
        STAR_SECTION = r"((?:\d+;?)*)"
        codeParts = code.split(" ")
        patternBuf = []
        for char in codeParts:
            if not char:
                continue
            if char == "esc":
                patternBuf.append("\\x1b")
            elif char == "***":
                patternBuf.append(STAR_SECTION)
            elif char == "**":
                patternBuf.append(r"(\d*)")

            else:
                patternBuf.append(re.escape(char))
        return "".join(patternBuf);

    def loadEscapeMap(self, escapeMap):
        for k, v in escapeMap.iteritems():
            self.addEscapeCode(k, v)

