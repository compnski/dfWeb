
escape_code_map = {
    # GFX sets
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

    "esc D" : ("index",),
    "esc M" : ("reverseIndex",),
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
