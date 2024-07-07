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


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1017, 710)
        self.oldPic = QtWidgets.QLabel(Form)
        self.oldPic.setGeometry(QtCore.QRect(110, 120, 320, 240))
        self.oldPic.setScaledContents(True)
        self.oldPic.setAlignment(QtCore.Qt.AlignCenter)
        self.oldPic.setObjectName("oldPic")
        self.newPic = QtWidgets.QLabel(Form)
        self.newPic.setGeometry(QtCore.QRect(570, 120, 320, 240))
        self.newPic.setScaledContents(True)
        self.newPic.setAlignment(QtCore.Qt.AlignCenter)
        self.newPic.setObjectName("newPic")
        self.upload = QtWidgets.QPushButton(Form)
        self.upload.setGeometry(QtCore.QRect(400, 460, 93, 28))
        self.upload.setObjectName("upload")
        self.transform = QtWidgets.QPushButton(Form)
        self.transform.setGeometry(QtCore.QRect(540, 460, 93, 28))
        self.transform.setObjectName("transform")
        self.save = QtWidgets.QPushButton(Form)
        self.save.setGeometry(QtCore.QRect(540, 530, 93, 28))
        self.save.setObjectName("save")
        self.style = QtWidgets.QToolButton(Form)
        self.style.setGeometry(QtCore.QRect(400, 530, 93, 28))
        self.style.setObjectName("style")

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
        self.style.setText(_translate("Form", "风格选择"))


class CycleGANApp(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.upload.clicked.connect(self.uploadImage)
        self.style.clicked.connect(self.chooseStyle)
        self.transform.clicked.connect(self.transformImage)
        self.save.clicked.connect(self.saveImage)
        self.transform.setEnabled(False)
        self.save.setEnabled(False)
        self.fileName = ''
        self.output_image = None
        self.model = None
        self.styleChoice = '梵高风格'  # 默认风格

    def uploadImage(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.xpm *.jpg *.jpeg)",
                                                       options=options)
        if self.fileName:
            self.oldPic.setPixmap(QPixmap(self.fileName))
            self.transform.setEnabled(True)

    def chooseStyle(self):
        items = ("梵高风格", "浮世绘风格", "网格风格", "彩笔风格")
        item, ok = QtWidgets.QInputDialog.getItem(self, "选择风格", "风格列表", items, 0, False)
        if ok and item:
            self.styleChoice = item

    def loadModel(self): # 加载模型
        opt = TestOptions().parse() # 解析命令行选项
        opt.name = self.styleChoice + '_cyclegan'  # 设置实验名称
        opt.model = 'cycle_gan'
        opt.no_dropout = True
        opt.phase = 'test'
        # 指定模型
        if self.styleChoice == "梵高风格":
            opt.checkpoints_dir = './checkpoints/aaa.pth'  # 指定模型
        if self.styleChoice == "浮世绘风格":
            opt.checkpoints_dir = './checkpoints/bbb.pth'  # 指定模型
        if self.styleChoice == "网格风格":
            opt.checkpoints_dir = './checkpoints/bbb.pth'  # 指定模型
        if self.styleChoice == "彩笔风格":
            opt.checkpoints_dir = './checkpoints/bbb.pth'  # 指定模型
        self.model = create_model(opt)
        self.model.setup(opt)
        self.model.eval()
        self.transform_function = get_transform(opt)
        
        
    def transformImage(self):
        if self.model is None:
            self.loadModel()

        input_image = cv2.imread(self.fileName)
        input_image = Image.fromarray(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
        input_image = self.transform_function(input_image).unsqueeze(0)

        with torch.no_grad():
            fake_image = self.model.netG_A(input_image)
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


if __name__ == '__main__':
    app = QApplication([])
    ex = CycleGANApp()
    ex.show()
    app.exec_()
