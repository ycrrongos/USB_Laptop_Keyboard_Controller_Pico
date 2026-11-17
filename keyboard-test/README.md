# USB Laptop Keyboard Controller (Pico) 逐键测试页

一个纯静态网页，用来逐键验证 Pico / QMK / KMK 键盘的实际 HID 输出。

## 用法

```bash
cd keyboard-test
python3 -m http.server 8765
# 浏览器打开 http://127.0.0.1:8765/
```

也可以直接打开 `index.html`，但建议用本地 HTTP 服务，浏览器对焦点和下载更稳定。

1. 把目标键盘插到电脑上，确认系统已经识别为键盘。
2. 点“开始测试”。
3. **只用目标键盘按**，页面保持焦点。
4. 按对了自动下一个；按错了会显示实际收到的 `event.code`；完全没反应点“没反应 / 跳过”。
5. 走完 86 键后导出 JSON/CSV。

## 结果含义

- `pass`：期望的 `event.code` 和实际收到的一致。
- `wrong`：收到了别的键，`receivedCode` / `receivedKey` 是实际值。
- `no-response`：没有收到 HID 事件，或用户点了“没反应”。
- `skipped`：Fn 等预期不会产生 HID 的键。

## 注意

- 浏览器分不清 Pico 键盘和笔记本自带键盘；测试时不要用自带键盘。
- Fn 是 KMK 层键，单独按没有 HID，直接跳过。
- PrtSc、Win/GUI、Alt 可能被桌面/浏览器截获；没反应就跳过。
- 页面失焦会暂停；点底部提示条继续。
- 预期键表在 `index.html` 的 `GROUPS` 里，换其他配列时改这里。
