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
gfx = False
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

with open("f.log") as f:
    while f:
        char = f.read(1)
        ret = outputParser.parseChar(char)
        if ret is not None:
            r = t.render(ret[0])
            r = t.render(ret[1])
            if g:
                g.sink()

