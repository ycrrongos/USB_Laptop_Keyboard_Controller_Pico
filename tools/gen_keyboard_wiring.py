#!/usr/bin/env python3
"""Generate the reference VPC-EA matrix tables (CSV + reference doc).

The working firmware and the corrected reversed-adapter doc are hand-maintained
in firmware/main.py and docs/keyboard-wiring.md.

Source of truth for the matrix is:
  Sony Vaio VPCEA Keyboard A-1765-621-A Matrix.pdf
  https://github.com/thedalles77/USB_Laptop_Keyboard_Controller

The generated files are written under firmware/ and docs/. The web app embeds
the same data; keep MATRIX/PINS in sync if this script changes.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 16 matrix rows, 8 matrix columns. Empty string means no key at that node.
MATRIX = [
    ["", "", "RShift", "", "", "", "LShift", ""],
    ["", "LCtrl", "", "", "", "RCtrl", "", ""],
    ["", "", "", "", "Fn", "", "", ""],
    ["Comma", "Period", "L", "O", "F11", "F10", "9", "0"],
    ["M", "B", "J", "I", "F9", "F8", "8", "U"],
    ["N", "K", "H", "G", "6", "F7", "7", "Y"],
    ["V", "C", "F", "T", "F6", "F5", "5", "R"],
    ["X", "A", "D", "E", "F4", "F3", "3", "4"],
    ["Z", "S", "W", "Q", "F2", "F1", "1", "2"],
    ["", "", "Space", "Semicolon", "Grave", "Esc", "Tab", "CapsLock"],
    ["Menu", "Slash", "", "", "Minus", "F12", "P", "LBr"],
    ["", "", "", "", "", "", "", "GUI"],
    ["AltR", "", "", "AltL", "", "", "", ""],
    ["", "", "Quote", "RBr", "PSCREEN", "NumLock", "Equal", ""],
    ["Left", "Down", "Right", "Up", "Home", "PgDn", "End", "PgUp"],
    ["", "Backslash", "", "Enter", "Delete", "Insert", "Backspace", ""],
]

# FPC pins 2..25 are the 24 scan lines; 1 and 26..32 are no-connect.
ROW_PINS = [2, 3, 4, 5, 6, 8, 11, 13, 14, 15, 16, 17, 18, 20, 21, 22]
COL_PINS = [7, 9, 10, 12, 19, 23, 24, 25]
ROW_GPIO = list(range(16))                  # GP0..GP15
COL_GPIO = [16, 17, 18, 19, 20, 21, 22, 28]  # GP16..GP22, GP28

# Physical pin numbers on the standard Pico / Pico H / Pico W / Pico 2
# 40-pin header. GND is at 3, 8, 13, 18, 23, 28, 33, 38.
GPIO_PHYS = {
    0: 1, 1: 2, 2: 4, 3: 5, 4: 6, 5: 7, 6: 9, 7: 10,
    8: 11, 9: 12, 10: 14, 11: 15, 12: 16, 13: 17, 14: 19, 15: 20,
    16: 21, 17: 22, 18: 24, 19: 25, 20: 26, 21: 27, 22: 29,
    26: 31, 27: 32, 28: 34,
}

LABELS = {
    "RShift": "Shift→", "LShift": "←Shift", "RCtrl": "Ctrl→", "LCtrl": "←Ctrl",
    "Fn": "Fn", "Menu": "Menu", "GUI": "GUI", "CapsLock": "Caps",
    "Grave": "` ~", "LBr": "[", "RBr": "]", "Backslash": "\\",
    "Quote": "'", "Semicolon": ";", "Comma": ",", "Period": ".",
    "Slash": "/", "PSCREEN": "PrtSc", "NumLock": "Num", "PgUp": "PgUp",
    "PgDn": "PgDn", "Esc": "Esc", "Tab": "Tab", "Space": "Space",
    "Enter": "Enter", "Backspace": "Bksp", "Delete": "Del", "Insert": "Ins",
    "Home": "Home", "End": "End", "Left": "←", "Right": "→",
    "Up": "↑", "Down": "↓", "Minus": "-", "Equal": "=",
}

KMK = {
    "RShift": "KC.RSHIFT", "LShift": "KC.LSHIFT",
    "RCtrl": "KC.RCTRL", "LCtrl": "KC.LCTRL",
    "Fn": "KC.MO(1)", "Menu": "KC.APPLICATION", "GUI": "KC.LGUI",
    "CapsLock": "KC.CAPSLOCK", "Grave": "KC.GRAVE",
    "LBr": "KC.LBRACKET", "RBr": "KC.RBRACKET", "Backslash": "KC.BACKSLASH",
    "Quote": "KC.QUOTE", "Semicolon": "KC.SEMICOLON",
    "Comma": "KC.COMMA", "Period": "KC.DOT", "Slash": "KC.SLASH",
    "PSCREEN": "KC.PSCREEN", "NumLock": "KC.NUMLOCK",
    "PgUp": "KC.PGUP", "PgDn": "KC.PGDN", "Esc": "KC.ESCAPE",
    "Tab": "KC.TAB", "Space": "KC.SPACE", "Enter": "KC.ENTER",
    "Backspace": "KC.BACKSPACE", "Delete": "KC.DELETE", "Insert": "KC.INSERT",
    "Home": "KC.HOME", "End": "KC.END", "Left": "KC.LEFT",
    "Right": "KC.RIGHT", "Up": "KC.UP", "Down": "KC.DOWN",
    "Minus": "KC.MINUS", "Equal": "KC.EQUAL",
    "AltR": "KC.RALT", "AltL": "KC.LALT",
}


def code_for(key: str) -> str:
    if not key:
        return "KC.NO"
    if key in KMK:
        return KMK[key]
    if key.isalpha() and len(key) == 1:
        return f"KC.{key}"
    if key.isdigit():
        return f"KC.N{key}"
    if key.startswith("F") and key[1:].isdigit():
        return f"KC.{key}"
    raise ValueError(f"no KMK code for {key!r}")


def display(key: str) -> str:
    if not key:
        return ""
    if key in LABELS:
        return LABELS[key]
    return key


def wiring_rows():
    rows = []
    for i, fpc in enumerate(ROW_PINS):
        rows.append((fpc, f"R{i}", ROW_GPIO[i], GPIO_PHYS[ROW_GPIO[i]], "行 row"))
    for i, fpc in enumerate(COL_PINS):
        rows.append((fpc, f"C{i}", COL_GPIO[i], GPIO_PHYS[COL_GPIO[i]], "列 column"))
    return sorted(rows)


def write_csv() -> None:
    import csv

    with (ROOT / "firmware" / "keyboard-wiring-reference.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["fpc_pin", "signal", "gpio", "physical_pin", "kind"])
        for fpc, signal, gpio, phys, kind in wiring_rows():
            w.writerow([fpc, signal, f"GP{gpio}", phys, kind])

    with (ROOT / "firmware" / "keymap.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["row", "col", "fpc_row_pin", "fpc_col_pin", "key", "kmk"])
        for r, row in enumerate(MATRIX):
            for c, key in enumerate(row):
                if key:
                    w.writerow(
                        [r, c, ROW_PINS[r], COL_PINS[c], display(key), code_for(key)]
                    )


def write_firmware() -> None:
    row_lines = "\n".join(
        f"    board.GP{gpio},  # FPC {fpc}  R{i}"
        for i, (fpc, gpio) in enumerate(zip(ROW_PINS, ROW_GPIO))
    )
    col_lines = "\n".join(
        f"    board.GP{gpio},  # FPC {fpc}  C{i}"
        for i, (fpc, gpio) in enumerate(zip(COL_PINS, COL_GPIO))
    )
    keymap_lines = "\n".join(
        "        [" + ", ".join(code_for(key) for key in row) + "],"
        for row in MATRIX
    )
    firmware = f'''# Aurora / Sony VAIO VPC-EA keyboard
# Matrix reference: A-1765-621-A, 32-pin FPC, pins 2-25 used.
# Hardware: Raspberry Pi Pico / Pico H / Pico W / Pico 2 (40-pin header)
# Firmware: CircuitPython + KMK
#
# Copy this file to CIRCUITPY/main.py, and copy the kmk/ package to the
# CIRCUITPY root. No 5V and no 3.3V goes to the keyboard matrix.

import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# Matrix rows: FPC pins 2,3,4,5,6,8,11,13,14,15,16,17,18,20,21,22
keyboard.row_pins = (
{row_lines}
)

# Matrix columns: FPC pins 7,9,10,12,19,23,24,25
keyboard.col_pins = (
{col_lines}
)

# Passive laptop membrane matrix, no diodes. Either orientation works;
# COL2ROW drives the eight column pins and reads the sixteen row pins.
keyboard.diode_orientation = DiodeOrientation.COL2ROW

_LAYER0 = [
{keymap_lines}
]

# Layer 1 is deliberately transparent. Fn is mapped to MO(1); add your
# brightness/volume/media keys here once the Fn combinations are known.
keyboard.keymap = [_LAYER0, [[KC.TRNS] * 8 for _ in range(16)]]

if __name__ == "__main__":
    keyboard.go()
'''
    (ROOT / "firmware" / "main.py").write_text(firmware)


def write_doc() -> None:
    table = "\n".join(
        f"| {fpc} | {signal} | GP{gpio} | {phys} | {kind} |"
        for fpc, signal, gpio, phys, kind in wiring_rows()
    )
    header = "| FPC 针脚 | 矩阵信号 | Pico GPIO | Pico 物理脚 | 类型 |\n|---:|---|---:|---:|---|"

    matrix_header = "| 行 \\ 列 | " + " | ".join(
        f"C{c} · FPC{pin} · GP{gpio}" for c, (pin, gpio) in enumerate(zip(COL_PINS, COL_GPIO))
    ) + " |"
    matrix_sep = "|---|" + "---|" * 8
    matrix_lines = []
    for r, row in enumerate(MATRIX):
        cells = [f"R{r} · FPC{ROW_PINS[r]} · GP{ROW_GPIO[r]}"]
        cells.extend(display(key) if key else "·" for key in row)
        matrix_lines.append("| " + " | ".join(cells) + " |")
    matrix_table = "\n".join([matrix_header, matrix_sep, *matrix_lines])

    key_rows = []
    for r, row in enumerate(MATRIX):
        for c, key in enumerate(row):
            if key:
                key_rows.append(
                    f"| {r} | {c} | {ROW_PINS[r]} | {COL_PINS[c]} | {display(key)} | `{code_for(key)}` |"
                )
    key_table = "\n".join(
        ["| R | C | FPC 行针 | FPC 列针 | 键 | KMK |", "|---:|---:|---:|---:|---|---|", *key_rows]
    )

    doc = f'''# VPC-EA 键盘 → Raspberry Pi Pico 接线

更新：2026-11-17。适用于标准 **Raspberry Pi Pico / Pico H / Pico W / Pico 2** 的 40 针排针（引脚顺序相同）。如果你买的是其他 RP2040 开发板，按它的引脚图把 GPIO 编号重新映射即可。

> 电气参考件是 **A-1765-621-A（黑色美式）**。白色采购件的排线走向可能相同，但焊线前必须用万用表核对本文的“按键—行/列”对应关系。不要把参考件的结论当成已核验的白色实物结论。

## 1. 先看结论

- 键盘排线是 **32 针 FPC**，但 **1 针和 26–32 针不连接**，实际只有 **2–25 针**共 24 条扫描线。
- 矩阵是 **16 行 × 8 列**，正好占 Pico 的 **24 个 GPIO**。
- 接线方案：**行 → GP0–GP15**，**列 → GP16–GP22 + GP28**。
- 键盘是无源开关矩阵，**不需要接 VCC 或 GND**；Pico 的 3.3V 只给 Pico 自己，绝不能接到矩阵线上。
- 接完后 Pico 还剩 **GP26、GP27** 两个可用 GPIO，正好是一对 I2C1（SDA/SCL），也能做 ADC 或普通数字口。

## 2. 接线总表

按 FPC 针脚从小到大接最不容易错：

{header}
{table}

Pico 的 GND 在物理脚 3、8、13、18、23、28、33、38，本接线不需要把它们接到键盘。

### Pico 端引脚对照

| GPIO | 物理脚 | 用途 |
|---:|---:|---|
| GP0–GP15 | 1,2,4,5,6,7,9,10,11,12,14,15,16,17,19,20 | 16 条行线 |
| GP16–GP22 | 21,22,24,25,26,27,29 | 7 条列线 |
| GP28 | 34 | 第 8 条列线（ADC2，可作数字口） |
| GP26 / GP27 | 31 / 32 | 预留（I2C1 SDA/SCL） |
| GND | 3,8,13,18,23,28,33,38 | 不接键盘 |
| 3V3(OUT) / VSYS / VBUS | 36 / 39 / 40 | 不接键盘 |

## 3. 矩阵图

行是 FPC 针脚 2–22 中的 16 条，列是 FPC 针脚 7–25 中的 8 条。格子里的文字是按键，`·` 表示该节点没有按键。

{matrix_table}

## 4. 转接板怎么用

1. 买 **32P FPC/FFC 转 2.54mm 排针、带锁扣、已焊接插座** 的转接板，确认间距是排线实际的 0.5 / 0.8 / 1.0mm，并确认是上接还是下接。
2. 排线 **1 针和 26–32 针不要接**。原作者特别提示：需要修掉 1 针附近的塑料，排线才能对齐插座；先空插确认，不要硬压。
3. 转接板上标 1–32 的丝印不一定和排线方向一致。用万用表通断档，从排线金手指逐根对到转接板排针，做好标记。
4. 杜邦线建议用不同颜色：行线一色、列线一色，GND/电源不接。线长控制在 15cm 以内，先搭面包板或直接焊排针。
5. 不要热插拔 FPC；插拔前断电。

## 5. 上电前用万用表验证

把键盘放平、排线插好但不接 Pico，用通断档按下列按键，确认闭合的是对应两根 FPC 针脚：

| 按键 | 应导通的 FPC 针脚 | 矩阵 |
|---|---|---|
| Q | 14 和 12 | R8 + C3 |
| Space | 15 和 10 | R9 + C2 |
| Esc | 15 和 23 | R9 + C5 |
| ← | 21 和 7 | R14 + C0 |
| Backspace | 22 和 24 | R15 + C6 |

只要有一组对不上，就先停下来重新核对排线方向，不要照着本文直接焊。

## 6. 固件

仓库里已经生成好 **KMK（CircuitPython）** 固件：

- `firmware/main.py`：16×8 矩阵、完整 86 键键位、Fn 占位层。
- `firmware/keymap.csv`：每个矩阵节点的键位和 KMK 键码，便于核对。
- `firmware/keyboard-wiring.csv`：接线表，便于打印。

使用步骤：

1. 给 Pico 刷 CircuitPython（按住 BOOTSEL 上电，拖入官方 `.uf2`）。
2. 把 KMK 的 `kmk/` 目录复制到 CIRCUITPY 根目录。
3. 把 `firmware/main.py` 复制成 `CIRCUITPY/main.py`。
4. 用 USB 接电脑，逐个按键测试；先测 Q、Space、Esc、方向键、Backspace。

Fn 目前只映射成 `MO(1)`，第 1 层是全透明占位；等确认这台键盘的 Fn 组合（亮度、音量、无线开关等）后再补。

## 7. 参考资料

- 矩阵与引脚：[Sony Vaio VPCEA Keyboard A-1765-621-A Matrix.pdf](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony%20Vaio%20VPCEA%20Keyboard%20A-1765-621-A%20Matrix.pdf)
- 原参考固件：[Sony_VPCEA_Keyboard_4p0.ino](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony_VPCEA_Keyboard_4p0.ino)
- Pico 数据手册：[pico-datasheet.pdf](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- KMK 键码：[KMK keycodes](https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md)

## 8. 完整键位表

{key_table}
'''
    (ROOT / "docs" / "keyboard-wiring-reference.md").write_text(doc)


def main() -> None:
    # The working firmware (firmware/main.py) is hand-maintained after the
    # reversed-adapter discovery; do not overwrite it here.
    write_csv()
    # write_firmware()
    write_doc()
    print(f"wrote {ROOT / 'docs' / 'keyboard-wiring-reference.md'}")
    print(f"wrote {ROOT / 'firmware' / 'keyboard-wiring-reference.csv'}")
    print(f"wrote {ROOT / 'firmware' / 'keymap.csv'}")


if __name__ == "__main__":
    main()
