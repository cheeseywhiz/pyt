import enum
import numpy as np
from ..run_terminal.TerminalStore import control_codes

__all__ = 'Mod', 'sym_table',


class BinUInt(np.uint):
    def __repr__(self):
        return bin(self)


class UIntFlagEnum(BinUInt, enum.Flag):
    pass


class Mod(UIntFlagEnum):
    Zero = 0
    Shift = enum.auto()
    Lock = enum.auto()
    Control = enum.auto()
    Mod1 = enum.auto()
    Mod2 = enum.auto()
    Mod3 = enum.auto()
    Mod4 = enum.auto()
    Mod5 = enum.auto()


Mod.lock_mods = Mod.Lock, Mod.Mod2  # Caps/Num lock


def escape_sequence(seq):
    return chr(control_codes.C0.ESC) + seq


def control_sequence(final_byte, *args, intermediate_byte=''):
    return ''.join([
        chr(control_codes.C1_7B.CSI),
        ';'.join(map(str, args)),
        ''.join(map(chr, [intermediate_byte, final_byte])),
    ])


# Adatpted from /usr/include/X11/keysymdef.h
#
# The "X11 Window System Protocol" standard defines in Appendix A the
# keysym codes. These 29-bit integer values identify characters or
# functions associated with each key (e.g., via the visible
# engraving) of a keyboard layout. This file assigns mnemonic macro
# names for these keysyms.
#
# Where a keysym corresponds one-to-one to an ISO 10646 / Unicode
# character, this is noted in a comment that provides both the U+xxxx
# Unicode position, as well as the official Unicode name of the
# character.

sym_table = {
    0x000000: '',  # NoSymbol
    0xffffff: '',  # VoidSymbol
    0xff08: chr(control_codes.C0.BS),  # BackSpace
    0xff09: '\t',  # Tab
    0xff0a: '\n',  # Linefeed
    0xff0b: '',  # Clear
    0xff0d: '\n',  # Return, enter
    0xff13: '',  # Pause
    0xff14: '',  # Scroll_Lock
    0xff15: '',  # Sys_Req
    0xff1b: '',  # Escape
    0xffff: '',  # Delete

    # International & multi-key character composition
    0xff20: '',  # Multi_key character compose
    0xff37: '',  # Codeinput
    0xff3c: '',  # SingleCandidate
    0xff3d: '',  # MultipleCandidate
    0xff3e: '',  # PreviousCandidate

    # Cursor control & motion
    0xff50: '\r',  # Home
    0xff51: '',  # Left, left arrow
    0xff52: '',  # Up, up arrow
    0xff53: '',  # Right, right arrow
    0xff54: '',  # Down, down arrow
    0xff55: '',  # Prior, previous
    0xff55: '',  # Page_Up
    0xff56: '',  # Next
    0xff56: '',  # Page_Down
    0xff57: '',  # End, EOL
    0xff58: '',  # Begin, BOL

    # Misc functions
    0xff60: '',  # Select, mark
    0xff61: '',  # Print
    0xff62: '',  # Execute, run, do
    0xff63: '',  # Insert, insert here
    0xff65: '',  # Undo
    0xff66: '',  # Redo, again
    0xff67: '',  # Menu
    0xff68: '',  # Find, search
    0xff69: '',  # Cancel, stop, abort, exit
    0xff6a: '',  # Help
    0xff6b: '',  # Break
    0xff7e: '',  # Mode_switch, Character set switch
    0xff7f: '',  # Num_Lock

    # Keypad functions, keypad numbers cleverly chosen to map to ASCII
    0xff80: '',  # Space
    0xff89: '',  # Tab
    0xff8d: '',  # Enter
    0xff91: '',  # F1
    0xff92: '',  # F2
    0xff93: '',  # F3
    0xff94: '',  # F4
    0xff95: '',  # Home
    0xff96: '',  # Left
    0xff97: '',  # Up
    0xff98: '',  # Right
    0xff99: '',  # Down
    0xff9a: '',  # Prior
    0xff9a: '',  # Page_Up
    0xff9b: '',  # Next
    0xff9b: '',  # Page_Down
    0xff9c: '',  # End
    0xff9d: '',  # Begin
    0xff9e: '',  # Insert
    0xff9f: '',  # Delete
    0xffbd: '',  # Equal
    0xffaa: '',  # Multiply
    0xffab: '',  # Add
    0xffac: '',  # Separator, often comma
    0xffad: '',  # Subtract
    0xffae: '',  # Decimal
    0xffaf: '',  # Divide

    0xffb0: '',  # KP_0
    0xffb1: '',  # KP_1
    0xffb2: '',  # KP_2
    0xffb3: '',  # KP_3
    0xffb4: '',  # KP_4
    0xffb5: '',  # KP_5
    0xffb6: '',  # KP_6
    0xffb7: '',  # KP_7
    0xffb8: '',  # KP_8
    0xffb9: '',  # KP_9

    # Auxiliary functions; note the duplicate definitions for left and right
    # function keys;  Sun keyboards and a few other manufacturers have such
    # function key groups on the left and/or right sides of the keyboard.
    # We've not found a keyboard with more than 35 function keys total.
    0xffbe: '',  # F1
    0xffbf: '',  # F2
    0xffc0: '',  # F3
    0xffc1: '',  # F4
    0xffc2: '',  # F5
    0xffc3: '',  # F6
    0xffc4: '',  # F7
    0xffc5: '',  # F8
    0xffc6: '',  # F9
    0xffc7: '',  # F10
    0xffc8: '',  # F11
    0xffc8: '',  # L1
    0xffc9: '',  # F12
    0xffc9: '',  # L2
    0xffca: '',  # F13
    0xffca: '',  # L3
    0xffcb: '',  # F14
    0xffcb: '',  # L4
    0xffcc: '',  # F15
    0xffcc: '',  # L5
    0xffcd: '',  # F16
    0xffcd: '',  # L6
    0xffce: '',  # F17
    0xffce: '',  # L7
    0xffcf: '',  # F18
    0xffcf: '',  # L8
    0xffd0: '',  # F19
    0xffd0: '',  # L9
    0xffd1: '',  # F20
    0xffd1: '',  # L10
    0xffd2: '',  # F21
    0xffd2: '',  # R1
    0xffd3: '',  # F22
    0xffd3: '',  # R2
    0xffd4: '',  # F23
    0xffd4: '',  # R3
    0xffd5: '',  # F24
    0xffd5: '',  # R4
    0xffd6: '',  # F25
    0xffd6: '',  # R5
    0xffd7: '',  # F26
    0xffd7: '',  # R6
    0xffd8: '',  # F27
    0xffd8: '',  # R7
    0xffd9: '',  # F28
    0xffd9: '',  # R8
    0xffda: '',  # F29
    0xffda: '',  # R9
    0xffdb: '',  # F30
    0xffdb: '',  # R10
    0xffdc: '',  # F31
    0xffdc: '',  # R11
    0xffdd: '',  # F32
    0xffdd: '',  # R12
    0xffde: '',  # F33
    0xffde: '',  # R13
    0xffdf: '',  # F34
    0xffdf: '',  # R14
    0xffe0: '',  # F35
    0xffe0: '',  # R15

    # Modifiers
    0xffe1: '',  # Shift_L, Left shift
    0xffe2: '',  # Shift_R, Right shift
    0xffe3: '',  # Control_L, Left control
    0xffe4: '',  # Control_R, Right control
    0xffe5: '',  # Caps_Lock, Caps lock
    0xffe6: '',  # Shift_Lock, Shift lock

    0xffe7: '',  # Meta_L, Left meta
    0xffe8: '',  # Meta_R, Right meta
    0xffe9: '',  # Alt_L, Left alt
    0xffea: '',  # Alt_R, Right alt
    0xffeb: '',  # Super_L, Left super
    0xffec: '',  # Super_R, Right super
    0xffed: '',  # Hyper_L, Left hyper
    0xffee: '',  # Hyper_R, Right hyper

    # Latin 1
    # (ISO/IEC 8859-Unicode: '',  # 1 U+0020..U+00FF)
    # Byte 0: '',  # 3
    0x0020: ' ',  # space  # U+0020 SPACE
    0x0021: '!',  # exclam  # U+0021 EXCLAMATION MARK
    0x0022: '"',  # quotedbl  # U+0022 QUOTATION MARK
    0x0023: '#',  # numbersign  # U+0023 NUMBER SIGN
    0x0024: '$',  # dollar  # U+0024 DOLLAR SIGN
    0x0025: '%',  # percent  # U+0025 PERCENT SIGN
    0x0026: '&',  # ampersand  # U+0026 AMPERSAND
    0x0027: '\'',  # apostrophe  # U+0027 APOSTROPHE
    0x0028: '(',  # parenleft  # U+0028 LEFT PARENTHESIS
    0x0029: ')',  # parenright  # U+0029 RIGHT PARENTHESIS
    0x002a: '*',  # asterisk  # U+002A ASTERISK
    0x002b: '+',  # plus  # U+002B PLUS SIGN
    0x002c: ',',  # comma  # U+002C COMMA
    0x002d: '-',  # minus  # U+002D HYPHEN-MINUS
    0x002e: '.',  # period  # U+002E FULL STOP
    0x002f: '/',  # slash  # U+002F SOLIDUS
    0x0030: '0',  # XK_0  # U+0030 DIGIT ZERO
    0x0031: '1',  # XK_1  # U+0031 DIGIT ONE
    0x0032: '2',  # XK_2  # U+0032 DIGIT TWO
    0x0033: '3',  # XK_3  # U+0033 DIGIT THREE
    0x0034: '4',  # XK_4  # U+0034 DIGIT FOUR
    0x0035: '5',  # XK_5  # U+0035 DIGIT FIVE
    0x0036: '6',  # XK_6  # U+0036 DIGIT SIX
    0x0037: '7',  # XK_7  # U+0037 DIGIT SEVEN
    0x0038: '8',  # XK_8  # U+0038 DIGIT EIGHT
    0x0039: '9',  # XK_9  # U+0039 DIGIT NINE
    0x003a: ':',  # colon  # U+003A COLON
    0x003b: ';',  # semicolon  # U+003B SEMICOLON
    0x003c: '<',  # less  # U+003C LESS-THAN SIGN
    0x003d: '=',  # equal  # U+003D EQUALS SIGN
    0x003e: '>',  # greater  # U+003E GREATER-THAN SIGN
    0x003f: '?',  # question  # U+003F QUESTION MARK
    0x0040: '@',  # at  # U+0040 COMMERCIAL AT
    0x0041: 'A',  # A  # U+0041 LATIN CAPITAL LETTER A
    0x0042: 'B',  # B  # U+0042 LATIN CAPITAL LETTER B
    0x0043: 'C',  # C  # U+0043 LATIN CAPITAL LETTER C
    0x0044: 'D',  # D  # U+0044 LATIN CAPITAL LETTER D
    0x0045: 'E',  # E  # U+0045 LATIN CAPITAL LETTER E
    0x0046: 'F',  # F  # U+0046 LATIN CAPITAL LETTER F
    0x0047: 'G',  # G  # U+0047 LATIN CAPITAL LETTER G
    0x0048: 'H',  # H  # U+0048 LATIN CAPITAL LETTER H
    0x0049: 'I',  # I  # U+0049 LATIN CAPITAL LETTER I
    0x004a: 'J',  # J  # U+004A LATIN CAPITAL LETTER J
    0x004b: 'K',  # K  # U+004B LATIN CAPITAL LETTER K
    0x004c: 'L',  # L  # U+004C LATIN CAPITAL LETTER L
    0x004d: 'M',  # M  # U+004D LATIN CAPITAL LETTER M
    0x004e: 'N',  # N  # U+004E LATIN CAPITAL LETTER N
    0x004f: 'O',  # O  # U+004F LATIN CAPITAL LETTER O
    0x0050: 'P',  # P  # U+0050 LATIN CAPITAL LETTER P
    0x0051: 'Q',  # Q  # U+0051 LATIN CAPITAL LETTER Q
    0x0052: 'R',  # R  # U+0052 LATIN CAPITAL LETTER R
    0x0053: 'S',  # S  # U+0053 LATIN CAPITAL LETTER S
    0x0054: 'T',  # T  # U+0054 LATIN CAPITAL LETTER T
    0x0055: 'U',  # U  # U+0055 LATIN CAPITAL LETTER U
    0x0056: 'V',  # V  # U+0056 LATIN CAPITAL LETTER V
    0x0057: 'W',  # W  # U+0057 LATIN CAPITAL LETTER W
    0x0058: 'X',  # X  # U+0058 LATIN CAPITAL LETTER X
    0x0059: 'Y',  # Y  # U+0059 LATIN CAPITAL LETTER Y
    0x005a: 'Z',  # Z  # U+005A LATIN CAPITAL LETTER Z
    0x005b: '[',  # bracketleft  # U+005B LEFT SQUARE BRACKET
    0x005c: '\\',  # backslash  # U+005C REVERSE SOLIDUS
    0x005d: ']',  # bracketright  # U+005D RIGHT SQUARE BRACKET
    0x005e: '^',  # asciicircum  # U+005E CIRCUMFLEX ACCENT
    0x005f: '_',  # underscore  # U+005F LOW LINE
    0x0060: '`',  # grave  # U+0060 GRAVE ACCENT
    0x0061: 'a',  # a  # U+0061 LATIN SMALL LETTER A
    0x0062: 'b',  # b  # U+0062 LATIN SMALL LETTER B
    0x0063: 'c',  # c  # U+0063 LATIN SMALL LETTER C
    0x0064: 'd',  # d  # U+0064 LATIN SMALL LETTER D
    0x0065: 'e',  # e  # U+0065 LATIN SMALL LETTER E
    0x0066: 'f',  # f  # U+0066 LATIN SMALL LETTER F
    0x0067: 'g',  # g  # U+0067 LATIN SMALL LETTER G
    0x0068: 'h',  # h  # U+0068 LATIN SMALL LETTER H
    0x0069: 'i',  # i  # U+0069 LATIN SMALL LETTER I
    0x006a: 'j',  # j  # U+006A LATIN SMALL LETTER J
    0x006b: 'k',  # k  # U+006B LATIN SMALL LETTER K
    0x006c: 'l',  # l  # U+006C LATIN SMALL LETTER L
    0x006d: 'm',  # m  # U+006D LATIN SMALL LETTER M
    0x006e: 'n',  # n  # U+006E LATIN SMALL LETTER N
    0x006f: 'o',  # o  # U+006F LATIN SMALL LETTER O
    0x0070: 'p',  # p  # U+0070 LATIN SMALL LETTER P
    0x0071: 'q',  # q  # U+0071 LATIN SMALL LETTER Q
    0x0072: 'r',  # r  # U+0072 LATIN SMALL LETTER R
    0x0073: 's',  # s  # U+0073 LATIN SMALL LETTER S
    0x0074: 't',  # t  # U+0074 LATIN SMALL LETTER T
    0x0075: 'u',  # u  # U+0075 LATIN SMALL LETTER U
    0x0076: 'v',  # v  # U+0076 LATIN SMALL LETTER V
    0x0077: 'w',  # w  # U+0077 LATIN SMALL LETTER W
    0x0078: 'x',  # x  # U+0078 LATIN SMALL LETTER X
    0x0079: 'y',  # y  # U+0079 LATIN SMALL LETTER Y
    0x007a: 'z',  # z  # U+007A LATIN SMALL LETTER Z
    0x007b: '{',  # braceleft  # U+007B LEFT CURLY BRACKET
    0x007c: '|',  # bar  # U+007C VERTICAL LINE
    0x007d: '}',  # braceright  # U+007D RIGHT CURLY BRACKET
    0x007e: '~',  # asciitilde  # U+007E TILDE
}
