import sys
import time

class BaseError(Error):pass
class NotImplementedError(BaseError):
    def __init__(self, functionName, *funtionArgs):
        super(NotImplementedError, self).__init__("%s(%s)" % (functionName, ", ".join(funtionArg))

class BaseTerminal(object):

    def __init__(self):
        #self.log = open("termdata.log", "w")
        self.t0 = int(time.time())

    def delay(self, delaytime):
        "Delay until relative time in seconds since start is less than the passed value"
        #print >>sys.stderr, "".join([r"\x%x" % ord(c) for c in delaytime])
        delaytime = struct.unpack("I", delaytime)[0]
        resumeTime = self.t0 + delaytime / 1000
        #print >>sys.stderr, resumeTime - int(time.time())
        while int(time.time() * 1000) < resumeTime:
            pass
        #print >>sys.stderr,'done'

    def render(self, object):
        "Takes either a string or action tuple and renders it"
        try:
            if type(object) is str:
                return self.printString(object)
            else:
            args = []
            for n in object[1:]:
                args.extend(n.split(";"))
            #print >>self.log, object
            getattr(self, object[0])(*args)
        except 
