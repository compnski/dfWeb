import outputparser
import sys
from data import *
from graphics import *
import time

outputParser = outputparser.OutputParser()
outputParser.loadEscapeMap(escape_code_map)
import termModel

#def __init__(self, glyphManager, gfxTerm, charGroup):

t = None
gfx = True
g = None
if gfx:
    glyphManager = GlyphManager()
    glyphManager.loadSprite(GlyphManager.VT220_GLYPH_FILENAME, 10, 8)
    g = GfxTerm()
    group = g.getSpriteGroup()
    gfxCharFactory = GfxCharFactory(glyphManager, g, group)
    t = termModel.Terminal(gfxCharFactory, 25, 80)
    g.setTermModel(t)
    t.setDisplay(g)
else:
    import terminalrenderer
    t = terminalrenderer.TerminalRenderer()

data = open("f.log").read()
for char in data:
    ret = outputParser.parseChar(char)
    if ret is not None:
        for cmd in ret:
            disp = t.render(cmd)
            if disp is not None:
                sys.stdout.write(disp)
        if g:
            g.sink()

