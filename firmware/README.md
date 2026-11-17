# USB Laptop Keyboard Controller (Pico) 固件

最终工作固件以本目录的 `main.py` 为准；矩阵来源是开源参考件 **A-1765-621-A**。

## 当前固件

- CircuitPython + KMK，16 行 × 8 列，扁平的 128 项 keymap。
- 扫描方式照原版 `Sony_VPCEA_Keyboard_4p0.ino`：列上拉输入，逐行拉低，其余行高阻；按下时列读到低。
- 本机转接板丝印与 FPC 反序（丝印 a = FPC 33-a），`main.py` 里的行/列 GPIO 已按反向重排。转接板 8–25 为原有 18 根，26–31 需补 6 根；详见 `docs/keyboard-wiring.md` 第 9 节。
- 实物左/右 Ctrl 与参考件相反，keymap 已在 R1C1 / R1C5 对调 `KC.LCTRL` / `KC.RCTRL`。
- Fn 层已实现：Fn+F2 静音、Fn+F3 音量减、Fn+F4 音量加、Fn+Insert 暂停、Fn+NumLock Scroll Lock。Fn 单独按不会产生 HID 事件，这是正常的。

## 使用

1. 给 Pico 刷 CircuitPython（BOOTSEL 上电，拖入官方 `.uf2`）。
2. 把 KMK 的 `kmk/` 目录复制到 `CIRCUITPY/` 根目录。
3. 把本目录的 `main.py` 复制到 `CIRCUITPY/main.py`。
4. USB 接电脑，用 `keyboard-test/index.html` 逐键测试。

## 键不响应时

先查 FPC 接触：转接板丝印和 FPC 反序，FPC 2–7 必须走丝印 26–31。用万用表从转接板排针量到 FPC 金手指，重点看 Shift/Ctrl 行和 C0 列。接触正常后再看 `docs/keyboard-wiring.md` 的反向表。
