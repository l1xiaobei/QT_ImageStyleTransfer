# 更新日志

## 0.0.1 (2024-7-7)

### 功能

+ 添加了`environment.yml`文件,可通过`conda env create -f environment.yml`来创建该项目所需要的虚拟环境。
+ 添加了`GUI`文件夹，用于存放GUI界面文件。
+ 添加了`pytorch-CycleGAN-and-pix2pix`文件夹，用于存放模型相关文件。

### 修改

+ 修改了许可证内容以满足所引用开源项目`https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix`的要求。

## 0.0.2 (2024-7-7)

### 功能

+ 重构代码组织结构，添加`code`文件夹来替代`GUI`与`pytorch-CycleGAN-and-pix2pix`文件夹。
+ 在`code`文件夹中添加了`main.py`， 实现图像迁移软件的基础逻辑。

### 修改

- 删除了`GUI`与`pytorch-CycleGAN-and-pix2pix`文件夹。
+ `environment.yml`文件中添加了`opencv-python`库以满足处理待转换图片的需求。

##  0.0.3 (2024-7-9)

### 修改

+ 修改`./code/data/unaligned_dataset.py`逻辑使得可以**分别**加载测试用的AB图片。
+ `./code/options/base_options.py`中添加参数`testA_dir、testB_dir`。
+ `./code/main.py`中添加了处理这两个新增参数的功能。
+ 修改了`./code/main.py`中的`opt.name`的处理逻辑以及其他很多地方，初步实现图像迁移。

## 0.0.4 (2024-8-7)

+ 引入silicon ui前的最后一次提交。

## 0.0.5 (2024-8-7)

### 功能
+ 添加了`./code/SiliconUI`文件夹，用于重构按钮为silicon控件
+ 添加了标题栏`self.window_title = QLabel(self)`。
+ 添加了`./code/img`文件夹用于存储软件logo。

### 修改

+ 修改`main.py`中的`setup`函数，将qt控件重构为silicon控件，将风格选择按钮由toolbutton更换为combobox。同时修改了风格选择按钮对应的槽函数。
+ 通过样式表`Form.setStyleSheet`修改了窗口背景颜色，以及将矩形变为圆角矩形

### 存在的问题

- *发现转换后的图片有可能会出现镜像翻转，目前对于出现原因以及解决方案尚不知悉。

## 0.0.6 (2024-8-8)

### 功能

+ 添加了一个[清屏]按钮用于清除当前图像显示框中的图像。
