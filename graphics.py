import pygame
from pygame.locals import *
import termModel

class GlyphManager(object):
    VT220_GLYPH_FILENAME = "vt220-rom.png"

    def __init__(self):
        pass

    def loadSprite(self, spriteFile, glyphHeight, glyphWidth):

        self.spriteImg = pygame.image.load(spriteFile)

        self.glyphWidth = glyphWidth
        self.glyphHeight = glyphHeight
        self.maxCol = self.spriteImg.get_width() / glyphWidth
        self.maxRow = self.spriteImg.get_height() / glyphHeight

    def getGlyph(self, charSet, char):
        if type(char) is str:
            char = ord(char)
        if char == 32:
            r, c = 0, 0
        else:
            r = char % self.maxRow
            c = char / 16

        return self.spriteImg.subsurface(
            pygame.Rect(c * self.glyphWidth, r * self.glyphHeight,
                        self.glyphWidth, self.glyphHeight))



class GfxCharFactory(object):

    def __init__(self, glyphManager, gfxTerm, charGroup):
        self.glyphManager = glyphManager
        self.gfxTerm = gfxTerm
        self.charGroup = charGroup


    @property
    def charHeight(self):
        return self.gfxTerm.height / self.gfxTerm.termModel.r

    @property
    def charWidth(self):
        return self.gfxTerm.width / self.gfxTerm.termModel.c

    def getChar(self, r, c, char, attrs):
        rect = Rect(c * self.charWidth, r * self.charHeight,
                    self.charWidth, self.charHeight)
        return GfxChar(char, self.glyphManager.getGlyph(0, char),
                       attrs, self.charGroup, rect)

class GfxChar(termModel.Char, pygame.sprite.DirtySprite):
    "A graphical sprit that represents a character."
    def __init__(self, char, glyph, attrs, spriteGroup, rect):
        super(GfxChar, self).__init__(char, attrs)
        super(pygame.sprite.DirtySprite, self).__init__(spriteGroup)
        self.attrs = attrs
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.HWSURFACE, 8)
        self.image.fill((255,255,255))
        self.image.blit(glyph, (0, 0))
        self.image.set_palette([self.attrs['fgColor'], self.attrs['bgColor']])
        self.dirty = 1
        self.add(spriteGroup)

    def setCoord(self, r, c):
        self.rect.top, self.rect.left = r * self.rect.height, c * self.rect.width

class GfxTerm(object):

    def getSpriteGroup(self):
        return self.group

    def loop(self):
        # Event loop
        self.running = True
        while self.running:
            self.sink()


    def sink(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            if not self._processEvent(event):
                return
            #d = self.termModel.getAndClearDirtySet()
            #if d:
            #self.updateDisplay([self._coordToRect(c) for c in d])

        self.group.update()
        #pygame.display.flip()
        pygame.display.update(self.group.draw(self.screen))

    def _processEvent(self, event):
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                        #Quit when you press Q
                return False
            if event.key == K_r:
                        #Restart the engine
                return True
            if event.key == K_z:
                for i in xrange(256):
                    self.termModel.printString(chr(i))
            if event.key == K_x:
                self.termModel.printString("".join([chr(i) for i in xrange(256)]))
            if event.key == K_h:
                self.termModel.printString("Hello World")
            if event.key == K_r:
                self.termModel.setRendition(32, 40)
            if event.key == K_c:
                self.termModel.eraseInScreen(2)
            if event.key == K_g:

                print self.group
                self.group.update()
                self.group.draw(self.screen)
                pygame.display.update()
                #self.termModel.setRendition(46, 34)
            if event.key == K_d:
                for r in self.termModel.termBuf:
                    print "".join(map(str,r))
                print len(self.termModel.termBuf), len(self.termModel.termBuf[0])

        return True

#                 if event.key == K_UP:
#                     self.player.moveup()
#                 if event.key == K_DOWN:
#                     self.player.movedown()
#                 if event.key == K_RIGHT:
#                     self.player.moveright()
#                 if event.key == K_LEFT:
#                     self.player.moveleft()
#        return True

#     def updateDisplay(self, dirtySet = None):
#         self.screen.fill((255,255,255))
#         for r in xrange(self.r):
#             for c in xrange(self.c):
#                 char = self.termModel.getChar(r,c)
#                 if char:
#                     self.screen.blit(self._getGlyph(char.char), (c * self.glyphWidth, r * self.glyphHeight))
#         pygame.display.update()

    def _coordToRect(self, coord):
        r, c = coord
        return Rect(c * self.glyphWidth, r * self.glyphHeight, self.glyphWidth, self.glyphHeight)

    def _getGlyph(self, char):
        try:
            return self._glyphCache[char]
        except KeyError:
            self._glyphCache[char] = self.glyphManager.getGlyph(0, char)
            return self._glyphCache[char]

    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.group = pygame.sprite.RenderUpdates()

#     def __init__(self):
#         self.height = height
#         self.width = width
#         self.running = True


    def setTermModel(self, termModel):
#        self._glyphCache = {}
        self.termModel = termModel
        self.r, self.c = termModel.r ,termModel.c
        self.width = self.c * 8
        self.height = self.r * 10
        self.glyphHeight = 10
        self.glyphWidth = 8
        self.screen = pygame.display.set_mode((self.width, self.height+10))
        self.screen.fill((255,255,255))
        self.area = pygame.rect.Rect(0, 0, self.width, self.height)
        pygame.display.set_caption("TERM")


if __name__ == "__main__":
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

    print 'z'
    g.loop()
    print 'z'
