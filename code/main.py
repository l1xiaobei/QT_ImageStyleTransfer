# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QLabel, QPushButton, QToolButton
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
import torch
from PIL import Image
from models import create_model
from options.test_options import TestOptions
from data.base_dataset import get_transform
# 与SiliconUI有关的库文件
#from SiliconUI.SiLayout import SiLayoutV
from SiliconUI import *
#from SiliconUI.SiGlobal import *
#from SiliconUI.SiSticker import SiSticker

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 640) # 窗口默认长宽

        #设置最小长宽
        self.setMinimumWidth(1000)
        self.setMinimumHeight(640)

        # 设置窗口背景颜色
        #Form.setStyleSheet('background-color:{}'.format(colorset.BG_GRAD_HEX[2]))
        #Form.setStyleSheet("background-color: #3D4E30;")
        Form.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(3,0,30, 1),stop:0.5 rgba(115,3,192, 1),stop:1 rgba(236,56,188, 1)
                    
                );
            }
        """)# stop:0 rgba(3,0,30, 1),stop:0.33 rgba(115,3,192, 1),stop:0.66 rgba(236,56,188, 1),  stop:1 rgba(253,239,249, 1)

        # 设置logo图标
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('./img/logo2.png'))
        #self.logo.setGeometry(68, 20, 24, 24)
        self.logo.setGeometry(28,20,26,26)
        self.logo.setStyleSheet("border-radius: 12px;")  # 设置圆角

        # 设置个标题栏试试
        self.window_title = QLabel(self)
        #self.window_title.setStyleSheet('color: {}'.format(colorset.TEXT_GRAD_HEX[1]))
        self.window_title.setGeometry(64, 0, 500, 64)
        self.window_title.setText('图像风格迁移软件(ver0.0.6)           created by 自动化2102李昊洋')
        self.window_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.window_title.setFont(SiliconUI.SiFont.font_L1_bold)
        self.window_title.setStyleSheet("color: white; background-color : transparent")  # 标题栏背景设置为透明的

        self.oldPic = QtWidgets.QLabel(Form)
        self.oldPic.setGeometry(QtCore.QRect(110, 120, 320, 240))
        self.oldPic.setScaledContents(True)
        self.oldPic.setAlignment(QtCore.Qt.AlignCenter)
        self.oldPic.setObjectName("oldPic")
        self.oldPic.setStyleSheet("background-color: rgba(33,16,127,128);border-radius: 12px;")# 设置颜色，以及变为圆角矩形

        self.newPic = QtWidgets.QLabel(Form)
        self.newPic.setGeometry(QtCore.QRect(570, 120, 320, 240))
        self.newPic.setScaledContents(True)
        self.newPic.setAlignment(QtCore.Qt.AlignCenter)
        self.newPic.setObjectName("newPic")
        self.newPic.setStyleSheet("background-color: rgba(33,16,127,128);border-radius: 12px;")# 设置颜色，以及变为圆角矩形

        # 创建clear按钮用于清除qlabel中的图片
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(830, 380, 47, 27))
        self.clear.setObjectName("clear")
        self.clear.setStyleSheet("""
            QPushButton {
                color: white;
                border-radius: 50%;
                border-style: ridge;
                border-color: #3d4b66;
                border-width: 5px;
                background-color: #3d4b66;      
            }
        """)
        #border-style属性分别有:none 定义无边框
        #hidden 与 "none" 相同。不过应用于表时除外，对于表，hidden 用于解决边框冲突。
        #dotted 定义点状边框。在大多数浏览器中呈现为实线。
        #dashed 定义虚线。在大多数浏览器中呈现为实线。
        #solid 定义实线。
        #double 定义双线。双线的宽度等于 border-width 的值。
        #groove 定义 3D 凹槽边框。其效果取决于 border-color 的值。
        #ridge 定义 3D 垄状边框。其效果取决于 border-color 的值。
        #inset 定义 3D inset 边框。其效果取决于 border-color 的值。
        #outset 定义 3D outset 边框。其效果取决于 border-color 的值。
        #inherit 规定应该从父元素继承边框样式。
        
        # 创建sibutton控件作为上传按钮
        #self.upload = QtWidgets.QPushButton(Form)
        self.upload = SiButton(Form)
        self.upload.setGeometry(QtCore.QRect(330, 460, 130, 32))
        self.upload.setObjectName("upload")
        #self.upload.setStyleSheet("border-radius: 20px;")# 设置为圆角矩形
        #self.upload.setStyleSheet("""
        #    SiButton {
        #        background-color: %s;
        #        color: %s;
        #        border-radius: 10px;
        #    }
        #    SiButton:hover {
        #        background-color: %s;
        #    }
        #    SiButton:pressed {
        #        background-color: %s;
        #    }
        #    """ % (colorset.BTN_NORM_HEX[0], colorset.BTN_NORM_TEXT_HEX, colorset.BTN_HL_HEX[0], colorset.BTN_HOLD_HEX[0]))

        # 创建sibutton控件作为风格转换按钮
        self.transform = SiButton(Form)
        self.transform.setGeometry(QtCore.QRect(540, 460, 130, 32))
        self.transform.setObjectName("transform")

        # 创建sibutton控件作为结果保存按钮
        self.save = SiButton(Form)
        self.save.setGeometry(QtCore.QRect(540, 530, 130, 32))
        self.save.setObjectName("save")

        # 创建sicombobox控件作为风格选择下拉菜单
        #self.style = QtWidgets.QToolButton(Form)
        self.style = SiComboBox(Form)
        self.style.setGeometry(QtCore.QRect(330, 530, 130, 32))
        #self.style.setObjectName("style")
        self.style.addOption("星月夜风格", 1)
        self.style.addOption("梵高风格", 2)
        self.style.addOption("浮世绘风格", 3)
        self.style.addOption("网格风格", 4)
        self.style.addOption("彩笔风格", 5)
        self.style.setOption("星月夜风格")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.oldPic.setText(_translate("Form", "原图"))
        self.newPic.setText(_translate("Form", "转换后图片"))
        self.upload.setText(_translate("Form", "上传图片"))
        self.transform.setText(_translate("Form", "开始转换"))
        self.save.setText(_translate("Form", "保存结果"))
        self.clear.setText(_translate("Form", "清屏"))
        #self.style.setText(_translate("Form", "风格选择"))


class CycleGANApp(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.upload.clicked.connect(self.uploadImage)
        #self.style.clicked.connect(self.chooseStyle) 由toolbutton改为combobox
        self.clear.clicked.connect(self.clr)
        self.style.textChanged.connect(self.chooseStyle)
        self.transform.clicked.connect(self.transformImage)
        self.save.clicked.connect(self.saveImage)
        self.transform.setEnabled(False)
        self.save.setEnabled(False)
        self.fileName = ''
        self.output_image = None
        self.model = None
        self.styleChoice = '星月夜风格'  # 默认风格

    def uploadImage(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.xpm *.jpg *.jpeg)",
                                                       options=options)
        if self.fileName:
            self.oldPic.setPixmap(QPixmap(self.fileName))
            self.transform.setEnabled(True)

    #槽函数定义，以接收textchanged发送的参数text
    def chooseStyle(self,text):
        self.styleChoice = text
        #items = ("星月夜风格","梵高风格", "浮世绘风格", "网格风格", "彩笔风格")
        #item, ok = QtWidgets.QInputDialog.getItem(self, "选择风格", "风格列表", items, 0, False)
        #if ok and item:
            #self.styleChoice = item

    def loadModel(self): # 加载模型
        opt = TestOptions().parse() # 解析命令行选项
        opt.model = 'cycle_gan'
        opt.dataset_mode = 'unaligned'
        opt.testB_dir = self.fileName
        opt.phase = 'test'
        # opt.dataroot = './datasets'
        # #opt.no_dropout = True
        #opt.name = self.styleChoice + '_results'  # 设置实验名称

        # 指定模型
        if self.styleChoice == "星月夜风格":
            opt.name = 'starrynight'  # 设置实验名称
            opt.testA_dir = './datasets/starrynight/testA/00440.jpg'
            opt.checkpoints_dir = './checkpoints/'  # 指定模型
        if self.styleChoice == "梵高风格":
            opt.name = 'vangogh'  # 设置实验名称
            opt.testA_dir = './datasets/vangogh/testA/00440.jpg'
            opt.checkpoints_dir = './checkpoints/'  # 指定模型
        if self.styleChoice == "浮世绘风格":
            opt.name = 'vangogh'  # 设置实验名称
            opt.testA_dir = 'a'
            opt.checkpoints_dir = './checkpoints/bbb.pth'  # 指定模型
        if self.styleChoice == "网格风格":
            opt.name = 'vangogh'  # 设置实验名称
            opt.testA_dir = 'a'
            opt.checkpoints_dir = './checkpoints/bbb.pth'  # 指定模型
        if self.styleChoice == "彩笔风格":
            opt.name = 'vangogh'  # 设置实验名称
            opt.testA_dir = 'a'
            opt.checkpoints_dir = './checkpoints/bbb.pth'  # 指定模型

         # 打印设置的参数以验证
        #print("Experiment Name: ", opt.name)
        #print("Model: ", opt.model)
        #print("Checkpoints Directory: ", opt.checkpoints_dir)
        #print("filename: ", self.fileName)
        #print("testB: ", opt.testB_dir)
        #print("testA: ", opt.testA_dir)

        self.model = create_model(opt)
        self.model.setup(opt)
        self.model.eval()
        self.transform_function = get_transform(opt)
        
        
    def transformImage(self):
        #if self.model is None:
        self.loadModel()

        input_image = cv2.imread(self.fileName)
        input_image = Image.fromarray(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
        input_image = self.transform_function(input_image).unsqueeze(0)

        with torch.no_grad():
            #fake_image = self.model.netG_A(input_image)
            fake_image = self.model.netG_B(input_image)
        fake_image = fake_image[0].cpu().float().numpy()
        fake_image = (np.transpose(fake_image, (1, 2, 0)) + 1) / 2.0 * 255.0
        fake_image = np.clip(fake_image, 0, 255).astype(np.uint8)
        fake_image = cv2.cvtColor(fake_image, cv2.COLOR_RGB2BGR)

        self.output_image = fake_image
        output_file = 'output_image.jpg'
        cv2.imwrite(output_file, fake_image)
        self.newPic.setPixmap(QPixmap(output_file))
        self.save.setEnabled(True)

    def saveImage(self):
        if self.output_image is not None:
            save_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Images (*.png *.xpm *.jpg *.jpeg)")
            if save_path:
                cv2.imwrite(save_path, self.output_image)
    
    def clr(self):
        self.newPic.setPixmap(QPixmap(None))  # 清除newPic的图像  
        self.oldPic.setPixmap(QPixmap(None))  # 清除oldPic的图像
        self.oldPic.setText("原图")
        self.newPic.setText("转换后图片")


if __name__ == '__main__':
    app = QApplication([])
    ex = CycleGANApp()
    ex.show()
    app.exec_()
