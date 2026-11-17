# VPC-EA 键盘 → Raspberry Pi Pico 接线

> **2026-11-17 实物更正：** 本次购买的 32P 转接板丝印与 FPC 针号反序（丝印 a 对应 FPC 33-a）。本文前面的“按 FPC 针脚接线”表只适用于丝印与 FPC 同向的转接板。本机实际接线见最后一节“反向转接板实物接线”。

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

| FPC 针脚 | 矩阵信号 | Pico GPIO | Pico 物理脚 | 类型 |
|---:|---|---:|---:|---|
| 2 | R0 | GP0 | 1 | 行 row |
| 3 | R1 | GP1 | 2 | 行 row |
| 4 | R2 | GP2 | 4 | 行 row |
| 5 | R3 | GP3 | 5 | 行 row |
| 6 | R4 | GP4 | 6 | 行 row |
| 7 | C0 | GP16 | 21 | 列 column |
| 8 | R5 | GP5 | 7 | 行 row |
| 9 | C1 | GP17 | 22 | 列 column |
| 10 | C2 | GP18 | 24 | 列 column |
| 11 | R6 | GP6 | 9 | 行 row |
| 12 | C3 | GP19 | 25 | 列 column |
| 13 | R7 | GP7 | 10 | 行 row |
| 14 | R8 | GP8 | 11 | 行 row |
| 15 | R9 | GP9 | 12 | 行 row |
| 16 | R10 | GP10 | 14 | 行 row |
| 17 | R11 | GP11 | 15 | 行 row |
| 18 | R12 | GP12 | 16 | 行 row |
| 19 | C4 | GP20 | 26 | 列 column |
| 20 | R13 | GP13 | 17 | 行 row |
| 21 | R14 | GP14 | 19 | 行 row |
| 22 | R15 | GP15 | 20 | 行 row |
| 23 | C5 | GP21 | 27 | 列 column |
| 24 | C6 | GP22 | 29 | 列 column |
| 25 | C7 | GP28 | 34 | 列 column |

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

| 行 \ 列 | C0 · FPC7 · GP16 | C1 · FPC9 · GP17 | C2 · FPC10 · GP18 | C3 · FPC12 · GP19 | C4 · FPC19 · GP20 | C5 · FPC23 · GP21 | C6 · FPC24 · GP22 | C7 · FPC25 · GP28 |
|---|---|---|---|---|---|---|---|---|
| R0 · FPC2 · GP0 | · | · | Shift→ | · | · | · | ←Shift | · |
| R1 · FPC3 · GP1 | · | ←Ctrl | · | · | · | Ctrl→ | · | · |
| R2 · FPC4 · GP2 | · | · | · | · | Fn | · | · | · |
| R3 · FPC5 · GP3 | , | . | L | O | F11 | F10 | 9 | 0 |
| R4 · FPC6 · GP4 | M | B | J | I | F9 | F8 | 8 | U |
| R5 · FPC8 · GP5 | N | K | H | G | 6 | F7 | 7 | Y |
| R6 · FPC11 · GP6 | V | C | F | T | F6 | F5 | 5 | R |
| R7 · FPC13 · GP7 | X | A | D | E | F4 | F3 | 3 | 4 |
| R8 · FPC14 · GP8 | Z | S | W | Q | F2 | F1 | 1 | 2 |
| R9 · FPC15 · GP9 | · | · | Space | ; | ` ~ | Esc | Tab | Caps |
| R10 · FPC16 · GP10 | Menu | / | · | · | - | F12 | P | [ |
| R11 · FPC17 · GP11 | · | · | · | · | · | · | · | GUI |
| R12 · FPC18 · GP12 | AltR | · | · | AltL | · | · | · | · |
| R13 · FPC20 · GP13 | · | · | ' | ] | PrtSc | Num | = | · |
| R14 · FPC21 · GP14 | ← | ↓ | → | ↑ | Home | PgDn | End | PgUp |
| R15 · FPC22 · GP15 | · | \ | · | Enter | Del | Ins | Bksp | · |

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

- `firmware/main.py`：16×8 矩阵、完整 86 键键位、Fn 媒体层。
- `firmware/keymap.csv`：每个矩阵节点的键位和 KMK 键码，便于核对。
- `firmware/keyboard-wiring-reference.csv`：参考矩阵的 FPC 接线表；本机反向接线见第 9 节。

使用步骤：

1. 给 Pico 刷 CircuitPython（按住 BOOTSEL 上电，拖入官方 `.uf2`）。
2. 把 KMK 的 `kmk/` 目录复制到 CIRCUITPY 根目录。
3. 把 `firmware/main.py` 复制成 `CIRCUITPY/main.py`。
4. 用 USB 接电脑，逐个按键测试；先测 Q、Space、Esc、方向键、Backspace。

Fn 层已实现原版固件的媒体功能：Fn+F2 静音、Fn+F3 音量减、Fn+F4 音量加、Fn+Insert 暂停、Fn+NumLock Scroll Lock。Fn 单独按不会产生 HID 事件，这是正常的。

> 实物更正：左/右 Ctrl 与参考件相反。固件已在 keymap 中对调 R1C1 / R1C5 的 `KC.LCTRL` / `KC.RCTRL`。下面的完整键位表是参考矩阵的标注，不是最终固件里的 Ctrl 位置。

## 7. 参考资料

- 矩阵与引脚：[Sony Vaio VPCEA Keyboard A-1765-621-A Matrix.pdf](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony%20Vaio%20VPCEA%20Keyboard%20A-1765-621-A%20Matrix.pdf)
- 原参考固件：[Sony_VPCEA_Keyboard_4p0.ino](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony_VPCEA_Keyboard_4p0.ino)
- Pico 数据手册：[pico-datasheet.pdf](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- KMK 键码：[KMK keycodes](https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md)

## 8. 完整键位表

| R | C | FPC 行针 | FPC 列针 | 键 | KMK |
|---:|---:|---:|---:|---|---|
| 0 | 2 | 2 | 10 | Shift→ | `KC.RSHIFT` |
| 0 | 6 | 2 | 24 | ←Shift | `KC.LSHIFT` |
| 1 | 1 | 3 | 9 | ←Ctrl | `KC.LCTRL` |
| 1 | 5 | 3 | 23 | Ctrl→ | `KC.RCTRL` |
| 2 | 4 | 4 | 19 | Fn | `KC.MO(1)` |
| 3 | 0 | 5 | 7 | , | `KC.COMMA` |
| 3 | 1 | 5 | 9 | . | `KC.DOT` |
| 3 | 2 | 5 | 10 | L | `KC.L` |
| 3 | 3 | 5 | 12 | O | `KC.O` |
| 3 | 4 | 5 | 19 | F11 | `KC.F11` |
| 3 | 5 | 5 | 23 | F10 | `KC.F10` |
| 3 | 6 | 5 | 24 | 9 | `KC.N9` |
| 3 | 7 | 5 | 25 | 0 | `KC.N0` |
| 4 | 0 | 6 | 7 | M | `KC.M` |
| 4 | 1 | 6 | 9 | B | `KC.B` |
| 4 | 2 | 6 | 10 | J | `KC.J` |
| 4 | 3 | 6 | 12 | I | `KC.I` |
| 4 | 4 | 6 | 19 | F9 | `KC.F9` |
| 4 | 5 | 6 | 23 | F8 | `KC.F8` |
| 4 | 6 | 6 | 24 | 8 | `KC.N8` |
| 4 | 7 | 6 | 25 | U | `KC.U` |
| 5 | 0 | 8 | 7 | N | `KC.N` |
| 5 | 1 | 8 | 9 | K | `KC.K` |
| 5 | 2 | 8 | 10 | H | `KC.H` |
| 5 | 3 | 8 | 12 | G | `KC.G` |
| 5 | 4 | 8 | 19 | 6 | `KC.N6` |
| 5 | 5 | 8 | 23 | F7 | `KC.F7` |
| 5 | 6 | 8 | 24 | 7 | `KC.N7` |
| 5 | 7 | 8 | 25 | Y | `KC.Y` |
| 6 | 0 | 11 | 7 | V | `KC.V` |
| 6 | 1 | 11 | 9 | C | `KC.C` |
| 6 | 2 | 11 | 10 | F | `KC.F` |
| 6 | 3 | 11 | 12 | T | `KC.T` |
| 6 | 4 | 11 | 19 | F6 | `KC.F6` |
| 6 | 5 | 11 | 23 | F5 | `KC.F5` |
| 6 | 6 | 11 | 24 | 5 | `KC.N5` |
| 6 | 7 | 11 | 25 | R | `KC.R` |
| 7 | 0 | 13 | 7 | X | `KC.X` |
| 7 | 1 | 13 | 9 | A | `KC.A` |
| 7 | 2 | 13 | 10 | D | `KC.D` |
| 7 | 3 | 13 | 12 | E | `KC.E` |
| 7 | 4 | 13 | 19 | F4 | `KC.F4` |
| 7 | 5 | 13 | 23 | F3 | `KC.F3` |
| 7 | 6 | 13 | 24 | 3 | `KC.N3` |
| 7 | 7 | 13 | 25 | 4 | `KC.N4` |
| 8 | 0 | 14 | 7 | Z | `KC.Z` |
| 8 | 1 | 14 | 9 | S | `KC.S` |
| 8 | 2 | 14 | 10 | W | `KC.W` |
| 8 | 3 | 14 | 12 | Q | `KC.Q` |
| 8 | 4 | 14 | 19 | F2 | `KC.F2` |
| 8 | 5 | 14 | 23 | F1 | `KC.F1` |
| 8 | 6 | 14 | 24 | 1 | `KC.N1` |
| 8 | 7 | 14 | 25 | 2 | `KC.N2` |
| 9 | 2 | 15 | 10 | Space | `KC.SPACE` |
| 9 | 3 | 15 | 12 | ; | `KC.SEMICOLON` |
| 9 | 4 | 15 | 19 | ` ~ | `KC.GRAVE` |
| 9 | 5 | 15 | 23 | Esc | `KC.ESCAPE` |
| 9 | 6 | 15 | 24 | Tab | `KC.TAB` |
| 9 | 7 | 15 | 25 | Caps | `KC.CAPSLOCK` |
| 10 | 0 | 16 | 7 | Menu | `KC.APPLICATION` |
| 10 | 1 | 16 | 9 | / | `KC.SLASH` |
| 10 | 4 | 16 | 19 | - | `KC.MINUS` |
| 10 | 5 | 16 | 23 | F12 | `KC.F12` |
| 10 | 6 | 16 | 24 | P | `KC.P` |
| 10 | 7 | 16 | 25 | [ | `KC.LBRACKET` |
| 11 | 7 | 17 | 25 | GUI | `KC.LGUI` |
| 12 | 0 | 18 | 7 | AltR | `KC.RALT` |
| 12 | 3 | 18 | 12 | AltL | `KC.LALT` |
| 13 | 2 | 20 | 10 | ' | `KC.QUOTE` |
| 13 | 3 | 20 | 12 | ] | `KC.RBRACKET` |
| 13 | 4 | 20 | 19 | PrtSc | `KC.PSCREEN` |
| 13 | 5 | 20 | 23 | Num | `KC.NUMLOCK` |
| 13 | 6 | 20 | 24 | = | `KC.EQUAL` |
| 14 | 0 | 21 | 7 | ← | `KC.LEFT` |
| 14 | 1 | 21 | 9 | ↓ | `KC.DOWN` |
| 14 | 2 | 21 | 10 | → | `KC.RIGHT` |
| 14 | 3 | 21 | 12 | ↑ | `KC.UP` |
| 14 | 4 | 21 | 19 | Home | `KC.HOME` |
| 14 | 5 | 21 | 23 | PgDn | `KC.PGDN` |
| 14 | 6 | 21 | 24 | End | `KC.END` |
| 14 | 7 | 21 | 25 | PgUp | `KC.PGUP` |
| 15 | 1 | 22 | 9 | \ | `KC.BACKSLASH` |
| 15 | 3 | 22 | 12 | Enter | `KC.ENTER` |
| 15 | 4 | 22 | 19 | Del | `KC.DELETE` |
| 15 | 5 | 22 | 23 | Ins | `KC.INSERT` |
| 15 | 6 | 22 | 24 | Bksp | `KC.BACKSPACE` |

## 9. 反向转接板实物接线（2026-11-17）

本机转接板丝印与 FPC 针号**反序**：丝印 `a` 对应 FPC `33-a`。现有 18 根线接在丝印 8–25，实际承载 FPC 25–8；FPC 2–7 需要从丝印 26–31 补线。Pico 端保持“丝印 a → G(a)”不变，固件已经按反向关系重排。

| 转接板丝印 | Pico GPIO | 物理脚 | 实际 FPC | 逻辑 | 说明 |
|---:|---:|---:|---:|---|---|
| 8 | GP5 | 7 | FPC 25 | C7 | 原有 |
| 9 | GP17 | 22 | FPC 24 | C6 | 原有 |
| 10 | GP18 | 24 | FPC 23 | C5 | 原有 |
| 11 | GP6 | 9 | FPC 22 | R15 | 原有 |
| 12 | GP19 | 25 | FPC 21 | R14 | 原有 |
| 13 | GP7 | 10 | FPC 20 | R13 | 原有 |
| 14 | GP8 | 11 | FPC 19 | C4 | 原有 |
| 15 | GP9 | 12 | FPC 18 | R12 | 原有 |
| 16 | GP10 | 14 | FPC 17 | R11 | 原有 |
| 17 | GP11 | 15 | FPC 16 | R10 | 原有 |
| 18 | GP12 | 16 | FPC 15 | R9 | 原有 |
| 19 | GP20 | 26 | FPC 14 | R8 | 原有 |
| 20 | GP13 | 17 | FPC 13 | R7 | 原有 |
| 21 | GP14 | 19 | FPC 12 | C3 | 原有 |
| 22 | GP15 | 20 | FPC 11 | R6 | 原有 |
| 23 | GP21 | 27 | FPC 10 | C2 | 原有 |
| 24 | GP22 | 29 | FPC 9 | C1 | 原有 |
| 25 | GP28 | 34 | FPC 8 | R5 | 原有 |
| 26 | GP16 | 21 | FPC 7 | C0 | 新线 |
| 27 | GP4 | 6 | FPC 6 | R4 | 新线 |
| 28 | GP3 | 5 | FPC 5 | R3 | 新线 |
| 29 | GP2 | 4 | FPC 4 | R2 | 新线 |
| 30 | GP1 | 2 | FPC 3 | R1 | 新线 |
| 31 | GP0 | 1 | FPC 2 | R0 | 新线 |

> 丝印 1 和 32 分别对应 FPC 32/1，都是 NC，不接。
