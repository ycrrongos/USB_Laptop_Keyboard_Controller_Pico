# USB Laptop Keyboard Controller (Pico)：调试笔记

这是 Frank Adams 的 [USB_Laptop_Keyboard_Controller](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller) 的 Pico 移植版调试笔记。本文记录从“键盘到货”到“86 键逐键验证”的完整过程，包括走过的弯路。想直接复现的读者可以只看 [README](../README.md) 和 [接线文档](keyboard-wiring.md)；这里解释为什么最后是这套方案。

## 1. 目标与选型

整机是“手机核心的笔记本”：手机负责计算和显示输出，外接屏幕、键盘、扩展坞和电源。键盘要求是普通的笔记本薄膜键盘，最终选了 **Sony VAIO VPC-EA 白色美式 86 键**，控制器用 **Raspberry Pi Pico（RP2040）**，跑 USB HID。

选 Pico 的原因：

- 26 个可用 GPIO，键盘矩阵 16 行 × 8 列 = 24 根，够用。
- USB 是芯片专用 D+/D−，不占 GPIO。
- CircuitPython + KMK 上手快，改键位不需要重新编译固件。
- 成本低，焊坏了换一块不心疼。

## 2. 电气参考

黑色参考件 **A-1765-621-A** 的资料：

- 32 针 FPC，**1 针和 26–32 针 NC**，实际使用 2–25 针。
- 16 行 × 8 列，86 键。
- 原作者的 Teensy 4.0 参考固件用“列上拉、逐行拉低、其余行高阻”的负逻辑扫描。

矩阵 PDF 和原固件：

- [Matrix PDF](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony%20Vaio%20VPCEA%20Keyboard%20A-1765-621-A%20Matrix.pdf)
- [Sony_VPCEA_Keyboard_4p0.ino](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony_VPCEA_Keyboard_4p0.ino)

白色采购件料号：`148792421` / `012-101A-3201-A` / `550102L05-203-G`。白色件没有背光，FPC 里没有键盘电源。

**重要：** 参考件是黑色美式，不能假设白色件的 Ctrl 左右位置、以及你买的转接板丝印方向完全一致。本机踩了两个差异：**转接板丝印反序**（转接板问题）和 **左右 Ctrl 反**（键盘实物差异）。

## 3. 第一版固件为什么“能读到一部分，但大部分键没反应”

最初用 KMK 默认写法：

```python
keyboard.row_pins = (...)
keyboard.col_pins = (...)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.keymap = [
    [ ... 16 行 × 8 列的嵌套列表 ... ],
]
```

看起来没问题，实际有三个坑叠在一起：

### 坑 1：KMK 默认扫描是正逻辑

KMK 默认的 `keypad.MatrixScanner` 走 CircuitPython `keypad.KeyMatrix`，用 `columns_to_anodes` 控制方向，本质是**正逻辑/下拉**扫描：驱动高电平，按下读到高。

这块笔记本键盘是**负逻辑/上拉**：列上拉，行拉低，按下读到低。

结果就是：有些键能碰巧读到，有些完全读不到；换 `COL2ROW` / `ROW2COL` 也不稳定。

最终方案：写一个很小的 `VpceaScanner`，照原版固件的方式扫描：

```python
# 列：输入 + Pull.UP
# 行：默认输入（高阻），逐行改成输出低，读完恢复输入
# 按下 = 列读到低
```

### 坑 2：KMK 的 keymap 是扁平的

KMK 的 `_find_key_in_map()` 是：

```python
key = self.keymap[layer][idx]
```

`idx = row * cols + col`。如果 `keymap[layer]` 是 16×8 的嵌套列表，`self.keymap[layer][idx]` 取到的是一整行列表，不是键码。它不会报错，但键盘不出字。

正确写法是每层一个 **128 项的扁平列表**：

```python
_LAYER0 = [
    KC.NO, KC.NO, KC.RSHIFT, ...,   # row 0, 8 个
    ...
]
keyboard.keymap = [_LAYER0, _LAYER1]
```

### 坑 3：`KC.APPLICATION` 不在基础 KMK

Menu 键用 `KC.APPLICATION` 会在启动时报：

```text
kmk.keys: Invalid key: APPLICATION
```

基础 KMK 没有这个别名；要么启用 international 扩展，要么手动建：

```python
from kmk.keys import KeyboardKey
MENU_KEY = KeyboardKey(code=101)
```

## 4. 转接板反序：最大的坑

### 症状

修完扫描和 keymap 后，键盘能出字了，但测试页显示大量 `no-response`，而且能响应的键成对错位：

- Q → Home
- F3 → Quote
- Backspace → C
- Home → Q
- 5 → Backslash
- A → Equal
- 左 Ctrl → 右 Ctrl

这些不是随机错位，而是像“整条线序偏了一段”。

### 定位

把测试页的 no-response 键按参考矩阵反推，缺失的正好是：

| 缺失 FPC 线 | 受影响的行/列 |
|---|---|
| FPC 2 | 左/右 Shift |
| FPC 3 | 左/右 Ctrl |
| FPC 4 | Fn |
| FPC 5 | `,` `.` `L` `O` `F11` `F10` `9` `0` |
| FPC 6 | `M` `B` `J` `I` `F9` `F8` `8` `U` |
| FPC 7 | 整列 C0 |
| FPC 15 | Space、`;`、`` ` ``、Esc、Tab、Caps |
| FPC 16 | Menu、`/`、`-`、F12、P、`[` |
| FPC 18 | 左/右 Alt |

**FPC 2–7 是连续的一段，正好在 pin 1 那一端。** 原作者在他的座子上需要修掉 pin 1 附近的塑料才能插到底，但这不是所有座子都必需——本机座子不修剪也能用。后来确认，本机 FPC 2–7 失联是转接板反序导致这几根线根本没接，不是排线没插到底。

进一步检查发现：**转接板丝印和 FPC 针号是反的**，即丝印 `a` 对应 FPC `33-a`。原来按丝印 2–25 接的线，实际承载的是 FPC 31–8；FPC 2–7 在丝印 26–31，根本没接。

### 修正

不需要重焊 24 根。保持 Pico 端不动，把 6 根线从丝印 2–7 挪到 31–26：

| 现在 | 挪到 | Pico 端 | 实际 FPC |
|---|---|---|---|
| 2 | 31 | GP0 | FPC 2 |
| 3 | 30 | GP1 | FPC 3 |
| 4 | 29 | GP2 | FPC 4 |
| 5 | 28 | GP3 | FPC 5 |
| 6 | 27 | GP4 | FPC 6 |
| 7 | 26 | GP16 | FPC 7 |

然后固件按反向关系重排行/列 GPIO。最终固件引脚：

```text
行: GP0 GP1 GP2 GP3 GP4 GP28 GP15 GP13
    GP20 GP12 GP11 GP10 GP9 GP7 GP19 GP6
列: GP16 GP22 GP21 GP14 GP8 GP18 GP17 GP5
```

详细表见 [keyboard-wiring.md 第 9 节](keyboard-wiring.md#9-反向转接板实物接线2026-11-17)。

## 5. 逐键测试页

一开始靠串口打印和聊天同步按键，失败了两次：脚本还没进 REPL，人已经把键按完了；或者串口调试打印把缓冲堵住。

最后改成浏览器测试页：

- 页面一次显示一个键。
- 浏览器监听 Pico 的 HID `keydown`。
- 按对自动下一个；按错显示实际 `event.code`；没反应点按钮。
- 结果导出 JSON。

这个页面直接定位了“哪些 FPC 线开路”和“哪些键成对错位”，比串口日志直观得多。

### 第一轮结果（反向修正前）

84/86 里大量 no-response，能响应的键成对错位（Q↔Home、F3↔Quote 等）。这份 JSON 是发现转接板反序的关键证据。

### 最终结果（反向修正 + Ctrl 对调后）

- 84/86 直接 pass。
- PrtSc：系统截屏占用，测试页看不到，键本身正常。
- Fn：KMK 层键，单独按没有 HID，正常。
- 左/右 Ctrl：实测与参考件相反，keymap 对调后正确。
- 其余全部 pass。

## 6. 最终固件的关键点

| 点 | 做法 |
|---|---|
| 扫描 | 列上拉，逐行拉低，其余行高阻 |
| 矩阵 | 16 × 8，128 项扁平 keymap |
| Menu | `KeyboardKey(code=101)` |
| Ctrl | R1C1 / R1C5 对调 `KC.LCTRL` / `KC.RCTRL` |
| Fn | `KC.MO(1)` + 媒体层 |
| Fn+F2 | 静音 |
| Fn+F3 | 音量减 |
| Fn+F4 | 音量加 |
| Fn+Insert | Pause |
| Fn+NumLock | Scroll Lock |

## 7. 可复用的检查清单

如果你也在改造笔记本键盘：

1. **先量转接板方向。** 丝印和 FPC 针号可能反；用通断档从排针量到金手指，不要凭丝印。
2. **先做 5 组通断测试**：Q、Space、Esc、←、Backspace。确认 FPC 插到底、锁扣压紧。
3. **确认逻辑极性。** 万用表或原厂固件能看出是上拉还是下拉；KMK 默认扫描不一定适用。
4. **KMK keymap 用扁平列表。** 每层 128 项，索引 `row*8+col`。
5. **先跑逐键测试页**，再谈键位微调；不要靠“盲按 + 串口日志”。
6. **生产固件去掉扫描循环里的 `print`**，避免 USB 串口缓冲堵住。
7. **左右修饰键要单独测。** 参考件的 L/R 不一定和实物一致。
8. **Fn 不是普通键。** 单独按没有 HID，必须做 layer。
9. **PrtSc/Win/Alt 可能被系统占用。** 测试页看不到不代表键坏。
10. **换转接板/换键盘后重新跑测试页。** 矩阵兼容不等于线序兼容。

## 8. 还没做的

- Fn 的亮度、无线开关等组合：需要看键帽图标；当前只实现了原版 media 矩阵里的五个。
- 手机触摸板模式：手机触控 → 相对鼠标移动、点击、拖拽、双指滚动。
- 整机结构：屏幕/驱动板/扩展坞/电源/外壳/转轴/散热。
- 如果换用同向转接板，固件行/列 GPIO 要改回同向表。

## 9. 参考资料

- [thedalles77/USB_Laptop_Keyboard_Controller](https://github.com/thedalles77/USB_Laptop_Keyboard_Controller)
- [KMK Firmware](https://github.com/KMKfw/kmk_firmware)
- [CircuitPython](https://circuitpython.org/)
- [Raspberry Pi Pico 文档](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
