import pygame


brightnessMap = {1:'bold',
                 2:'dim'
                 }

black = pygame.Color('black')
red = pygame.Color('red')
green = pygame.Color('green')
yellow = pygame.Color('yellow')
green = pygame.Color('green')
blue = pygame.Color('blue')
magenta = pygame.Color('magenta')
cyan = pygame.Color('cyan')
white = pygame.Color('white')

colorMap = {0:(black.r, black.g, black.b),
            1:(red.r, red.g, red.b),
            2:(green.r, green.b, green.g),
            3:(yellow.r, yellow.b, yellow.g),
            4:(blue.r, blue.b, blue.g),
            5:(magenta.r, magenta.b, magenta.g),
            6:(cyan.r, cyan.b, cyan.g),
            7:(white.r, white.b, white.g)
            }

escape_code_map = {
    # GFX sets
    "esc D *X" : ("delay",),
    "esc ( A" : ("switchCharset", "UK-g0"),
    "esc ) A" : ("switchCharset", "UK-g1"),
    "esc ( B" : ("switchCharset", "ASCII-g0"),
    "esc ) B" : ("switchCharset", "ASCII-g1"),
    "esc * B" : ("switchCharset", "ASCII-g2"),
    "esc + B" : ("switchCharset", "ASCII-g3"),
    "esc ( 0" : ("switchCharset", "DEC-g0"),
    "esc ) 0" : ("switchCharset", "DEC-g1"),

    "esc [ *** m" : ("setRendition",),
    "esc [ *** h" : ("setMode",),
    "esc [ *** l" : ("resetMode",),

    "esc [ ? ** h" : ("setExpandedMode",),
    "esc [ ? ** l" : ("resetExpandedMode",),

    "esc = " : ("setKeypad", "application"),
    "esc > " : ("setKeypad", "numeric"),

    "esc [ ** ; ** r" : ("scrollRegion",),
    "esc [ ** A" : ("moveCursor", "up"),
    "esc [ ** B" : ("moveCursor", "down"),
    "esc [ ** C" : ("moveCursor", "left"),
    "esc [ ** D" : ("moveCursor", "right"),

    "esc [ A" : ("moveCursor", "up"),
    "esc [ B" : ("moveCursor", "down"),
    "esc [ C" : ("moveCursor", "left"),
    "esc [ D" : ("moveCursor", "right"),

    "esc [ ** ; ** H" : ("setCursorPos",),
    "esc [ ** ; ** f" : ("setCursorPos",),
    "esc [ H" : ("setCursorPos",),
    "esc [ f" : ("setCursorPos",),

    "esc D" : ("scrollUp",),
    "esc M" : ("scrollDown",),
    "esc E" : ("nextLine",),

    "esc 7" : ("saveCursor",),
    "esc 8" : ("restoreCursor",),

    "esc H" : ("setTabstop",),
    "esc g" : ("clearTabstop",),
    "esc 0 g" : ("clearTabstop",),
    "esc 3 g" : ("clearAllTabstops",),
    "esc c" : ("reset",),
    "esc [ ! p": ("fullReset",),

    "esc [ K" : ("eraseInLine", "",),
    "esc [ ** K" : ("eraseInLine",),
#    "esc [ ** K ": ("erase", "TO_BOL"),
#    "esc [ ** K ": ("erase", "LINE"),

    "esc [ J ": ("eraseInScreen", ""),
    "esc [ ** J ": ("eraseInScreen",),
#    "esc [ ** J ": ("erase", "TO_BOS"),
#    "esc [ ** J ": ("erase", "SCREEN"),

    "esc [ ** c" : ("getDevAttributes",),
    "esc [ ** n" : ("getDevStaus",),

    "esc [ ** P" : ("deleteChar",),
    "esc [ ** L" : ("insertLine",),
    "esc [ ** M" : ("deleteLine",),
    "esc [ ** @" : ("insertChar",),
    "esc [ ** X" : ("eraseChar",),
    }
