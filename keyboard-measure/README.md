# USB Laptop Keyboard Controller (Pico) 布局测绘台

一个纯静态网页，用来按毫米记录 VAIO VPC-EA 键盘的物理布局，并导出 JSON / SVG。

## 用法

```bash
cd keyboard-measure/dist
python3 -m http.server 8766
# 浏览器打开 http://127.0.0.1:8766/
```

也可以直接打开 `dist/index.html`。

## 功能

- 主体宽/深、边距、圆角、行 Y、缩进。
- 每行按键增删、单键宽高/圆角/位置编辑、拖动。
- 选中键后可编辑左/右边界 X、行 Y、宽高、圆角。
- 同步尺寸到本行右侧、同步 X/Y 间距、撤销。
- 导出 JSON 布局和真实毫米尺寸的 SVG（可导入 FreeCAD / Inkscape）。
- 右上角“接线 / 固件”页：FPC 接线表、16×8 矩阵图、KMK 固件和接线 CSV 下载。
- 数据自动存在浏览器 localStorage；支持导入/导出 JSON。

## 默认基准

示例默认值采用 **300mm 行宽 / 15×15mm 普通键 / 4mm 间距**。旧数据可以点“套用实测基准 300 / 15 / 4”更新，特殊宽度键和自定义 X 位置会保留。

## 说明

- SVG 是键帽投影和主体轮廓，不是可直接打印的承托件。
- 页面里的“下载 KMK main.py”是当前反向转接板工作固件，不是通用模板；换硬件时请同步修改引脚。
- 部署到静态托管时，`dist/` 就是站点根目录。
