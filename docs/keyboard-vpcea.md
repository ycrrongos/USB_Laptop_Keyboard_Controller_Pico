# VAIO VPC-EA 白色键盘：建模输入调查

更新：2026-11-14。项目选型：白色 VPCEA 内置键盘，RP2040 USB 控制器。尚未核对用户购买件的实物料号；以下不是完成的机械图纸。

接线与固件：见 [keyboard-wiring.md](keyboard-wiring.md)（2026-11-17，Pico 16×8 矩阵与 KMK 固件）。

> 2026-11-17 电气验证完成：白色实物与参考矩阵兼容；实物差异是**转接板丝印反序**和**左右 Ctrl 反**。86 键逐键测试通过，详见 [project-notes.md](project-notes.md)。

## 型号与版本

白色美式商品资料：148792421，012-101A-3201-A，550102L05-203-G。
来源：https://www.pchub.com/sony-vaio-vpcea-series-keyboard-148792421-us-white-p136584
同系列有带框/无框、US/UK/其他语言与替换件版本，不能用系列名保证轮廓、固定点和矩阵完全相同。

开源电气参考：A-1765-621-A。该料号对应黑色美式参考件，不能写成已验证白色采购件料号。
来源：https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/tree/master/Example_Keyboards/Sony_Vaio_VPCEA

## 参考件已确认电气信息

原作者 Matrix.pdf：32针排线，1和26–32无连接，2–25共24条扫描线；16行、8列。作者曾修剪靠近1脚的排线塑料以对齐插座。矩阵与VPCCW参考件相同。以上只适用于作者参考件，白色采购件待连续性核验。
排线间距、厚度、端部宽度和接触面方向未由已读原始材料确认，不指定转接插座型号。
原矩阵：https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony%20Vaio%20VPCEA%20Keyboard%20A-1765-621-A%20Matrix.pdf
固件：https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Sony_Vaio_VPCEA/Sony_VPCEA_Keyboard_4p0.ino

## 机械尺寸调查结果

未找到可靠且有测量边界的裸键盘工程尺寸图、孔位坐标图或CAD。
长宽、含键帽总厚、框体厚度、凸耳/螺柱高度、固定点坐标、排线出口及长度、键帽最高包络均未确认。
不按商品照片比例推算精确尺寸，不按通用19mm键距推导安装开口。
商家出现360×120×10mm数值，但未区分包装、裸件或带框件，未独立佐证，不用于CAD。
索尼维修手册入口（可用于继续核对装配结构，不构成尺寸图）：https://www.manualslib.com/manual/2949752/Sony-Vaio-Vpcea-Series.html

## 最少实物输入

1. 背面标签照片，确认购买件完整料号；正反面垂直照片，旁放直尺。
2. 最大宽和前后深：分别记录主体、外框、凸耳的边界。
3. 底面到未按压最高键帽的厚度，以及背面凸起的高度。
4. 固定孔/螺柱/插舌的位置与尺寸；以正面左前角为XY基准，背面照注意镜像。
5. 排线出口位置、可用长度、触点数、首末触点中心距、端部宽厚和接触面。

## 对建模的约束

在上述尺寸缺失时，只能建立标注未定尺寸的布局占位，不能发布可打印的键盘承托/固定槽。
实物确认后优先做独立可拆键盘托架，底面承托、固定件不压键帽或排线。公差通过小样确定。
