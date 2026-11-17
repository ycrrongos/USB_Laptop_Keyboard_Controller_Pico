# USB Laptop Keyboard Controller (Pico) / Sony VAIO VPC-EA keyboard
# Pico port of Frank Adams' USB_Laptop_Keyboard_Controller.
# Matrix reference: A-1765-621-A, 32-pin FPC, pins 2-25 used.
# Hardware: Raspberry Pi Pico / Pico H / Pico W / Pico 2 (40-pin header)
# Firmware: CircuitPython + KMK
#
# The scan method is ported from the original Sony_VPCEA_Keyboard_4p0.ino:
# columns are inputs with pull-ups, one row is driven low at a time, and the
# other rows are left hi-Z. A pressed key reads low on its column.
#
# This build has a REVERSED FPC adapter: adapter silk pin a carries FPC pin
# 33-a. The pin lists below are mapped for that reversal. Adapter pins 26-31
# still need wires to GP0..GP4 and GP16 for FPC 2-7.

import board
import digitalio
import time
from keypad import Event as KeyEvent

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, KeyboardKey
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.scanners import Scanner

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


class VpceaScanner(Scanner):
    def __init__(self, row_pins, col_pins):
        self.rows = [digitalio.DigitalInOut(p) for p in row_pins]
        self.cols = [digitalio.DigitalInOut(p) for p in col_pins]
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
        for col in self.cols:
            col.direction = digitalio.Direction.INPUT
            col.pull = digitalio.Pull.UP
        self.old = [[False] * len(self.cols) for _ in self.rows]

    @property
    def key_count(self):
        return len(self.rows) * len(self.cols)

    def scan_for_changes(self):
        for r, row in enumerate(self.rows):
            row.direction = digitalio.Direction.OUTPUT
            row.value = False
            time.sleep(0.00001)
            for c, col in enumerate(self.cols):
                pressed = not col.value
                if pressed != self.old[r][c]:
                    self.old[r][c] = pressed
                    row.direction = digitalio.Direction.INPUT
                    if pressed:
                        led.value = True
                        time.sleep(0.05)
                        led.value = False
                    time.sleep(0.01)
                    return KeyEvent(r * len(self.cols) + c, pressed)
            row.direction = digitalio.Direction.INPUT
        time.sleep(0.005)
        return None


keyboard = KMKKeyboard()
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

keyboard.row_pins = (
    board.GP0,   # adapter 31 -> FPC 2   R0  (new wire)
    board.GP1,   # adapter 30 -> FPC 3   R1  (new wire)
    board.GP2,   # adapter 29 -> FPC 4   R2  (new wire)
    board.GP3,   # adapter 28 -> FPC 5   R3  (new wire)
    board.GP4,   # adapter 27 -> FPC 6   R4  (new wire)
    board.GP28,  # adapter 25 -> FPC 8   R5
    board.GP15,  # adapter 22 -> FPC 11  R6
    board.GP13,  # adapter 20 -> FPC 13  R7
    board.GP20,  # adapter 19 -> FPC 14  R8
    board.GP12,  # adapter 18 -> FPC 15  R9
    board.GP11,  # adapter 17 -> FPC 16  R10
    board.GP10,  # adapter 16 -> FPC 17  R11
    board.GP9,   # adapter 15 -> FPC 18  R12
    board.GP7,   # adapter 13 -> FPC 20  R13
    board.GP19,  # adapter 12 -> FPC 21  R14
    board.GP6,   # adapter 11 -> FPC 22  R15
)

keyboard.col_pins = (
    board.GP16,  # adapter 26 -> FPC 7   C0  (new wire)
    board.GP22,  # adapter 24 -> FPC 9   C1
    board.GP21,  # adapter 23 -> FPC 10  C2
    board.GP14,  # adapter 21 -> FPC 12  C3
    board.GP8,   # adapter 14 -> FPC 19  C4
    board.GP18,  # adapter 10 -> FPC 23  C5
    board.GP17,  # adapter 9  -> FPC 24  C6
    board.GP5,   # adapter 8  -> FPC 25  C7
)

keyboard.matrix = VpceaScanner(keyboard.row_pins, keyboard.col_pins)

# Flat keymap: index = row * 8 + col, matching VpceaScanner.key_number.
MENU_KEY = KeyboardKey(code=101)

_LAYER0 = [
    KC.NO, KC.NO, KC.RSHIFT, KC.NO, KC.NO, KC.NO, KC.LSHIFT, KC.NO,
    KC.NO, KC.RCTRL, KC.NO, KC.NO, KC.NO, KC.LCTRL, KC.NO, KC.NO,
    KC.NO, KC.NO, KC.NO, KC.NO, KC.MO(1), KC.NO, KC.NO, KC.NO,
    KC.COMMA, KC.DOT, KC.L, KC.O, KC.F11, KC.F10, KC.N9, KC.N0,
    KC.M, KC.B, KC.J, KC.I, KC.F9, KC.F8, KC.N8, KC.U,
    KC.N, KC.K, KC.H, KC.G, KC.N6, KC.F7, KC.N7, KC.Y,
    KC.V, KC.C, KC.F, KC.T, KC.F6, KC.F5, KC.N5, KC.R,
    KC.X, KC.A, KC.D, KC.E, KC.F4, KC.F3, KC.N3, KC.N4,
    KC.Z, KC.S, KC.W, KC.Q, KC.F2, KC.F1, KC.N1, KC.N2,
    KC.NO, KC.NO, KC.SPACE, KC.SEMICOLON, KC.GRAVE, KC.ESCAPE, KC.TAB, KC.CAPSLOCK,
    MENU_KEY, KC.SLASH, KC.NO, KC.NO, KC.MINUS, KC.F12, KC.P, KC.LBRACKET,
    KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.LGUI,
    KC.RALT, KC.NO, KC.NO, KC.LALT, KC.NO, KC.NO, KC.NO, KC.NO,
    KC.NO, KC.NO, KC.QUOTE, KC.RBRACKET, KC.PSCREEN, KC.NUMLOCK, KC.EQUAL, KC.NO,
    KC.LEFT, KC.DOWN, KC.RIGHT, KC.UP, KC.HOME, KC.PGDN, KC.END, KC.PGUP,
    KC.NO, KC.BACKSLASH, KC.NO, KC.ENTER, KC.DELETE, KC.INSERT, KC.BACKSPACE, KC.NO,
]

# Fn layer, ported from the original media matrix:
#   Fn+F2 mute, Fn+F3 volume down, Fn+F4 volume up,
#   Fn+Insert pause, Fn+NumLock scroll lock.
_LAYER1 = [KC.TRNS] * 128
_LAYER1[60] = KC.VOLU       # R7C4  F4
_LAYER1[61] = KC.VOLD       # R7C5  F3
_LAYER1[68] = KC.MUTE       # R8C4  F2
_LAYER1[109] = KC.SCROLLLOCK  # R13C5 NumLock
_LAYER1[125] = KC.PAUSE     # R15C5 Insert
keyboard.keymap = [_LAYER0, _LAYER1]

if __name__ == "__main__":
    keyboard.go()
