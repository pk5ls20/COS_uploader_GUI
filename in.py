# 原始
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'in.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.、

# 引用
import source_rc
import os
import sys
import linecache
import atexit
from threading import Thread
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
from faker import Faker
import os
from Encryptor import enc
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PySide2.QtCore import Signal, QObject
from typing import List, Union

# 初始化变量
f = Faker(locale='zh_CN')
a_key: List[Union[int, str]] = [0] * 1000
a_pas = ''
fileaddress = [0] * 1
filepath = [0] * 10000
isok = 0
loglevel = 0
logging.basicConfig(filename="test1.log", filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
logging.debug("初始化变量完成！")
# 设置日志等级
class statuschange(QObject):
    sc = Signal(QStatusBar, str)


class updatex(QObject):
    pb1c = Signal(QProgressBar, int)


# 重制TextBrowser为拖拽作准备
class MyTB(QTextBrowser):
    global fileaddress

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        fileaddress[0] = (event.mimeData().urls()[0].toLocalFile())
        logging.debug('Now Dragpath is ' + str(fileaddress[0]))
        # print(fileaddress[0])
    logging.debug("TextBrowser拖拽重写完成！")


# 加载主窗口
class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.paths = ""
        self.setupUi(self)
        self.retranslateUi(self)
        self.setAcceptDrops(True)  # ==> 必须设置、
        self.save_stdout = sys.stdout
        sys.stdout = self
        self.ups = updatex()
        self.ups.pb1c.connect(self.changeint)

    def changeint(self, sf, num):
        sf.setValue(int(num))
        # logging.debug('changeint/sf/num'+str(sf)+str(num))

    # 输出重写
    def write(self, message):
        logging.info(message)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(378, 275)
        MainWindow.setMaximumSize(QtCore.QSize(378, 275))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWeiget_main = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWeiget_main.setGeometry(QtCore.QRect(0, 0, 371, 260))
        self.tabWeiget_main.setMaximumSize(QtCore.QSize(371, 260))
        self.tabWeiget_main.setBaseSize(QtCore.QSize(371, 251))
        self.tabWeiget_main.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWeiget_main.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWeiget_main.setObjectName("tabWeiget_main")
        self.select = QtWidgets.QWidget()
        self.select.setAccessibleName("")
        self.select.setObjectName("select")
        self.TB1_main = MyTB(self.select)
        self.TB1_main.setGeometry(QtCore.QRect(40, 10, 291, 121))
        self.TB1_main.setAcceptDrops(True)
        self.TB1_main.setAutoFillBackground(True)
        self.TB1_main.setObjectName("TB1_main")
        self.Lb1_uploadto = QtWidgets.QLabel(self.select)
        self.Lb1_uploadto.setGeometry(QtCore.QRect(40, 150, 48, 16))
        self.Lb1_uploadto.setObjectName("Lb1_uploadto")
        self.CB1_bucket = QtWidgets.QComboBox(self.select)
        self.CB1_bucket.setGeometry(QtCore.QRect(93, 150, 141, 19))
        self.CB1_bucket.setObjectName("CB1_bucket")
        self.PB1 = QtWidgets.QProgressBar(self.select)
        self.PB1.setGeometry(QtCore.QRect(40, 180, 301, 20))
        self.PB1.setProperty("value", 0)
        self.PB1.setObjectName("PB1")
        self.B1_upload = QtWidgets.QPushButton(self.select)
        self.B1_upload.setGeometry(QtCore.QRect(250, 150, 75, 23))
        self.B1_upload.setObjectName("B1_upload")
        self.B1_upload.setEnabled(False)
        # self.lb1l_status = QtWidgets.QLabel(self.select)
        # self.lb1l_status.setGeometry(QtCore.QRect(10, 210, 171, 16))
        # self.lb1l_status.setObjectName("lb1l_status")
        self.tabWeiget_main.addTab(self.select, "")
        self.output = QtWidgets.QWidget()
        self.output.setObjectName("output")
        self.TB2_output = QtWidgets.QTextBrowser(self.output)
        self.TB2_output.setGeometry(QtCore.QRect(20, 10, 331, 181))
        self.TB2_output.setObjectName("TB2_output")
        self.CB2_isautoclear = QtWidgets.QCheckBox(self.output)
        self.CB2_isautoclear.setGeometry(QtCore.QRect(30, 200, 68, 16))
        self.CB2_isautoclear.setObjectName("CB2_isautoclear")
        self.B2_clearall = QtWidgets.QPushButton(self.output)
        self.B2_clearall.setGeometry(QtCore.QRect(270, 200, 75, 23))
        self.B2_clearall.setObjectName("B2_clearall")
        self.tabWeiget_main.addTab(self.output, "")
        self.secret = QtWidgets.QWidget()
        self.secret.setObjectName("secret")
        self.groupBox = QtWidgets.QGroupBox(self.secret)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 361, 171))
        self.groupBox.setObjectName("groupBox")
        self.LB3_region = QtWidgets.QLabel(self.groupBox)
        self.LB3_region.setGeometry(QtCore.QRect(10, 150, 36, 16))
        self.LB3_region.setObjectName("LB3_region")
        self.LE3_mykey = QtWidgets.QLineEdit(self.groupBox)
        self.LE3_mykey.setGeometry(QtCore.QRect(80, 41, 161, 20))
        self.LE3_mykey.setEchoMode(QLineEdit.Password)
        self.LE3_mykey.setObjectName("LE3_mykey")
        self.LE3_mykey.EchoMode(QLineEdit.Password)
        self.LE3_sid = QtWidgets.QLineEdit(self.groupBox)
        self.LE3_sid.setGeometry(QtCore.QRect(80, 71, 161, 20))
        self.LE3_sid.setObjectName("LE3_sid")
        self.LB3_skey = QtWidgets.QLabel(self.groupBox)
        self.LB3_skey.setGeometry(QtCore.QRect(9, 97, 58, 16))
        self.LB3_skey.setObjectName("LB3_skey")
        self.LE3_skey = QtWidgets.QLineEdit(self.groupBox)
        self.LE3_skey.setGeometry(QtCore.QRect(80, 96, 161, 20))
        self.LE3_skey.setObjectName("LE3_skey")
        self.LB3_sec = QtWidgets.QLabel(self.groupBox)
        self.LB3_sec.setGeometry(QtCore.QRect(9, 42, 88, 16))
        self.LB3_sec.setObjectName("LB3_sec")
        self.LB3_sid = QtWidgets.QLabel(self.groupBox)
        self.LB3_sid.setGeometry(QtCore.QRect(9, 72, 52, 16))
        self.LB3_sid.setObjectName("LB3_sid")
        self.LE3_region = QtWidgets.QLineEdit(self.groupBox)
        self.LE3_region.setGeometry(QtCore.QRect(80, 150, 161, 20))
        self.LE3_region.setObjectName("LE3_region")
        self.LB3_bucket = QtWidgets.QLabel(self.groupBox)
        self.LB3_bucket.setGeometry(QtCore.QRect(10, 120, 36, 16))
        self.LB3_bucket.setObjectName("LB3_bucket")
        self.B3_save = QtWidgets.QPushButton(self.groupBox)
        self.B3_save.setGeometry(QtCore.QRect(260, 110, 91, 31))
        self.B3_save.setObjectName("B3_save")
        self.B3_load = QtWidgets.QPushButton(self.groupBox)
        self.B3_load.setGeometry(QtCore.QRect(260, 60, 91, 31))
        self.B3_load.setObjectName("B3_load")
        self.LB3_1_loadfilename = QtWidgets.QLabel(self.groupBox)
        self.LB3_1_loadfilename.setGeometry(QtCore.QRect(80, 20, 261, 16))
        self.LB3_1_loadfilename.setObjectName("LB3_1_loadfilename")
        self.LB3_1_now_load = QtWidgets.QLabel(self.groupBox)
        self.LB3_1_now_load.setGeometry(QtCore.QRect(10, 20, 341, 16))
        self.LB3_1_now_load.setObjectName("LB3_1_now_load")
        self.LE3_bucket = QtWidgets.QLineEdit(self.groupBox)
        self.LE3_bucket.setGeometry(QtCore.QRect(80, 120, 151, 20))
        self.LE3_bucket.setObjectName("LE3_bucket")
        self.B3_quebucket = QtWidgets.QPushButton(self.groupBox)
        self.B3_quebucket.setGeometry(QtCore.QRect(230, 120, 16, 21))
        self.B3_quebucket.setObjectName("B3_quebucket")
        self.groupBox_2 = QtWidgets.QGroupBox(self.secret)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 180, 361, 51))
        self.groupBox_2.setObjectName("groupBox_2")
        self.CB3_2_israndomname = QtWidgets.QCheckBox(self.groupBox_2)
        self.CB3_2_israndomname.setGeometry(QtCore.QRect(20, 20, 103, 23))
        self.CB3_2_israndomname.setObjectName("CB3_2_israndomname")
        self.CB3_2_islog = QtWidgets.QCheckBox(self.groupBox_2)
        self.CB3_2_islog.setGeometry(QtCore.QRect(130, 23, 68, 16))
        self.CB3_2_islog.setObjectName("CB3_2_islog")
        self.CB3_2_loglevel = QtWidgets.QComboBox(self.groupBox_2)
        self.CB3_2_loglevel.setGeometry(QtCore.QRect(201, 22, 60, 19))
        self.CB3_2_loglevel.setEditable(False)
        self.CB3_2_loglevel.setDuplicatesEnabled(False)
        self.CB3_2_loglevel.setObjectName("CB3_2_loglevel")
        self.CB3_2_loglevel.addItem("")
        self.CB3_2_loglevel.addItem("")
        self.CB3_2_loglevel.addItem("")
        self.CB3_2_save = QtWidgets.QPushButton(self.groupBox_2)
        self.CB3_2_save.setGeometry(QtCore.QRect(266, 22, 71, 21))
        self.CB3_2_save.setObjectName("CB3_2_save")
        self.tabWeiget_main.addTab(self.secret, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 378, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # self.statusbar.showMessage('Test Message')
        self.tabWeiget_main.setCurrentIndex(0)
        logging.debug("窗口绘制完毕")

        # 初始化槽函数
        self.tabWeiget_main.currentChanged.connect(self.tabchange)
        self.B3_load.clicked.connect(self.click_B3)
        self.B1_upload.clicked.connect(self.click_B1)
        self.B2_clearall.clicked.connect(self.click_B2)
        self.CB3_2_save.clicked.connect(self.click_CB3_2)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        logging.debug("槽函数编写完成")

    # 绘制UI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TB1_main.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><title>设置一个居中的图片</title><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimHei\';\"><br /></p>\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/pic/in.svg\" width=\"120\" height=\"80\" /><span style=\" font-family:\'SimHei\';\"> </span></p>\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimHei\';\">将文件拖拽到此处，或 </span><span style=\" font-family:\'SimHei\'; font-weight:600; color:#00007f;\">点击上传</span></p></body></html>"))
        self.Lb1_uploadto.setText(_translate("MainWindow", "上传至："))
        self.B1_upload.setText(_translate("MainWindow", "开始上传"))
        self.statusbar.showMessage('等待加载参数...')
        self.tabWeiget_main.setTabText(self.tabWeiget_main.indexOf(self.select), _translate("MainWindow", "上传"))
        self.CB2_isautoclear.setText(_translate("MainWindow", "自动清空"))
        self.B2_clearall.setText(_translate("MainWindow", "清空"))
        self.tabWeiget_main.setTabText(self.tabWeiget_main.indexOf(self.output), _translate("MainWindow", "输出"))
        self.groupBox.setTitle(_translate("MainWindow", "Config"))
        self.LB3_region.setText(_translate("MainWindow", "Region"))
        self.LB3_skey.setText(_translate("MainWindow",
                                         "<html><head/><body><p><span style=\" color:#aa0000; vertical-align:super;\">*</span>secretkey</p></body></html>"))
        self.LB3_sec.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" color:#aa0000; vertical-align:super;\">*</span>MyKey</p></body></html>"))
        self.LB3_sid.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" color:#aa0000; vertical-align:super;\">*</span>secretid</p></body></html>"))
        self.LB3_bucket.setText(_translate("MainWindow", "Bucket"))
        self.B3_save.setText(_translate("MainWindow", "SaveConfig"))
        self.B3_load.setText(_translate("MainWindow", "LoadConfig"))
        self.LB3_1_loadfilename.setText(_translate("MainWindow", "UNKNOWN"))
        self.LB3_1_now_load.setText(_translate("MainWindow", "当前加载为："))
        self.B3_quebucket.setText(_translate("MainWindow", "?"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Profile"))
        self.CB3_2_israndomname.setText(_translate("MainWindow", "随机文件名上传"))
        self.CB3_2_islog.setText(_translate("MainWindow", "输出日志"))
        self.CB3_2_loglevel.setItemText(0, _translate("MainWindow", "0-简单"))
        self.CB3_2_loglevel.setItemText(1, _translate("MainWindow", "1-基本"))
        self.CB3_2_loglevel.setItemText(2, _translate("MainWindow", "2-详细"))
        self.CB3_2_loglevel.setCurrentIndex(1)
        self.CB3_2_save.setText(_translate("MainWindow", "Save"))
        self.tabWeiget_main.setTabText(self.tabWeiget_main.indexOf(self.secret),
                                       _translate("MainWindow", "参数配置"))
        logging.debug("UI重绘完成")

    # 事件：切换到参数窗口
    def judgepath(self, path):
        # 0文件夹 1文件
        if os.path.isdir(path):
            logging.debug("judgepath=0")
            return 0
        elif os.path.isfile(path):
            logging.debug("judgepath=1")
            return 1

    def tabchange(self):
        global a_key
        global a_pas
        global setlevel
        logging.debug("Tabchange!")
        # 初始化页面
        if self.tabWeiget_main.currentIndex() == 2:
            # 把之前的writeio拆开写，当存在文件时
            if a_key[0] == 0 or a_pas == '':  # 不存在变量
                logging.info("self.LB3_1_now_load.setText('请创建/打开一个参数文件！')")
                self.LB3_1_now_load.setText('请创建/打开一个参数文件！')
                self.LB3_1_loadfilename.setText('')

    def click_CB3_2(self):
        # 输出日志事件
        global loglevel
        if self.CB3_2_islog.isChecked() == True:
            logger = logging.getLogger()
            if self.CB3_2_loglevel.currentIndex() == 0:
                logger.setLevel(logging.ERROR)
                loglevel = 0
            if self.CB3_2_loglevel.currentIndex() == 1:
                logger.setLevel(logging.INFO)
                loglevel = 1
            if self.CB3_2_loglevel.currentIndex() == 2:
                logger.setLevel(logging.DEBUG)
                loglevel = 2
        logging.debug('日志事件创建完成！等级'+str(loglevel))
        QMessageBox.information(self, "提示", '参数' + str(loglevel) + '保存成功！')
        logging.info(str(loglevel) + '保存成功！')

    # 事件：点击B3
    def click_B2(self):
        self.TB2_output.clear()
        logging.debug("CLEAR!")

    def click_B3(self):
        global isok
        COSfilename_e, fd = QFileDialog.getOpenFileName(self, '选择一个py文件', './',
                                                        '参数文件(*.secret.enc)', '参数文件(*.secret.enc)')
        if self.LE3_mykey.text() == '':  # 用户没有输入Mykey，弹窗提醒输入
            logging.info("Lost MyKey")
            QMessageBox.warning(self, "警告", "请输入MyKey！", QMessageBox.Cancel)
        else:
            if COSfilename_e != '':
                enc.decrypt_file(COSfilename_e)
                logging.debug('decryptd'+str(COSfilename_e))
                # writein COS.secret in a_key
                # 这块要重写
                COSfilename = COSfilename_e[:-4]
                logging.debug('COSfilename='+str(COSfilename))
                with open(COSfilename, 'r', encoding='UTF-8') as file:
                    time_cos = 0
                    for line in file:
                        a_key[time_cos] = line.strip()
                        logging.debug('分割原始参数中，a_key[time_cos]'+str(a_key[time_cos])+str(time_cos))
                        time_cos = time_cos + 1
                enc.encrypt_file(COSfilename)
                logging.debug('decryptd'+str(COSfilename))
                # 到此步，已将COS.secret加载到变量中，下一步开始比对密码值
                if self.LE3_mykey.text() == a_key[1]:  # 密码正确
                    # 开始加载变量
                    self.LB3_1_now_load.setText('当前加载为：')
                    self.LB3_1_loadfilename.setText(COSfilename)
                    self.LE3_mykey.setText(str(a_key[1]))
                    self.LE3_sid.setText(str(a_key[2]))
                    self.LE3_skey.setText(str(a_key[3]))
                    self.LE3_region.setText(str(a_key[4]))
                    self.LE3_bucket.setText(str(a_key[5]))
                    isok = 1
                    QMessageBox.information(self, "提示", "参数加载成功！")
                    self.statusbar.showMessage('参数加载成功！')
                    logging.info("参数加载成功！")
                    self.B1_upload.setEnabled(True)
                    # 将参数加载到第一页的选择库栏
                    # 首先将bucket分割，后赋值给a_key
                    list1: list[str] = str(a_key[5]).split(';')
                    timel = int(5)
                    for i in list1:
                        a_key[timel] = i
                        timel = timel + 1
                        logging.debug('开始转移参数'+str(timel))
                    # 进行一个参数的加载
                    self.CB1_bucket.addItems(list1)
                    logging.debug("参数已全部加载")
                else:
                    QMessageBox.warning(self, "注意", "Mykey校验未通过，请重新输入！", QMessageBox.Cancel)
                    self.statusbar.showMessage('Mykey校验未通过，请重新输入！')
                    logging.info("Mykey校验未通过，请重新输入！")
            else:
                QMessageBox.warning(self, "警告", "请选择文件", QMessageBox.Cancel)
                self.statusbar.showMessage('请选择文件！')
                logging.info("警告, 请选择文件")

    # 尝试用双多线程改写

    # 函数：进度条回调，计算当前上传的百分比
    def upload_percentage(self, consumed_bytes, total_bytes):
        # 进度条回调函数，计算当前上传的百分比
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            logging.debug('回传进度Rate='+str(rate))
            self.ups.pb1c.emit(self.PB1, int(rate))
            logging.debug("发送信号Rate")

    # 搬来的上传文件函数
    def uploadfile(self, filepathall, isfak):
        global timex
        global address
        global addressl
        try:
            ##### -----1.连接桶部分-----#####
            logging.debug('上传文件：loglevel='+ str(loglevel))
            if loglevel == 1:
                logging.basicConfig(level=logging.INFO, stream=sys.stdout)  # 输出日志，可以去掉qwq
            if loglevel == 2:
                logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
            self.statusbar.showMessage('开始上传！')
            logging.info("开始上传")
            # stream=self.TB2_output.append()
            config = CosConfig(Region=a_key[4], SecretId=a_key[2],
                               SecretKey=a_key[3], Token=None, Scheme='https')  # type: ignore
            logging.debug(str(a_key[4])+'/'+str(a_key[2])+'/'+str(a_key[3]))
            client = CosS3Client(config)
            ##### -----2.引入分割文件名os-----#####
            (ext, filename) = os.path.splitext(filepathall)
            fileext = filename
            logging.debug('fileext=' + str(fileext))
            (path, filename) = os.path.split(filepathall)
            filepath0 = path
            logging.debug('path=' + str(path))

            ##### -----3.询问随机文件名-----#####
            if isfak != 65536:
                filename = f.pystr() + fileext
                logging.debug('filename=' + str(filename))
            # addressl[timex] = filepathall

            ##### -----4.判断桶种有无重名项（跳过）-----#####
            ##### -----5.开始上传-----#####

            self.statusbar.showMessage('开始上传' + filepathall + '啦~', 5)
            logging.info('开始上传' + str(filepathall) + '啦~')
            # 主要的上传函数
            self.response = client.upload_file(
                Bucket=bucketx,
                Key=filename,
                LocalFilePath=filepathall,
                EnableMD5=False,
                progress_callback=self.upload_percentage
            )
            ##### -----6.总结-----#####
            self.statusbar.showMessage(filepathall + '上传成功！', 5)
            logging.info(str(filepathall) + '上传成功！')
            """
            if lib == 1:
                address[timex] = 'https://' + a_key[3] + '.cos.' + a_key[2] + '.myqcloud.com/' + filename
                timex = timex + 1
            if lib == 2:
                address[timex] = 'https://' + a_key[4] + '.cos.' + a_key[2] + '.myqcloud.com/' + filename
                timex = timex + 1
            """
        except (CosServiceError, CosClientError):
            self.statusbar.showMessage('上传COS中出现异常，请确定参数是否正确以及网络是否畅通')
            logging.info('上传COS中出现异常，请确定参数是否正确以及网络是否畅通')

    # 事件：点击B1
    def click_B1(self):
        global fileaddress
        global bucketx
        global isallfak
        # 检验环境变量是否存在
        bucketx = (self.CB1_bucket.currentText())
        logging.debug('bucketx='+str(bucketx))
        if isok == 1:
            # 可以上传，先看路径是文件还是文件夹
            if self.judgepath(fileaddress[0]) == 1:
                # 询问用户名移到这里
                isfak = QMessageBox.question(self, "COS_uploader", "是否使用随机文件名？（建议图床使用）",
                                             QMessageBox.Yes | QMessageBox.No)
                thread = Thread(target=self.uploadfile,
                                args=(fileaddress[0], isfak))
                logging.debug('子进程uploadfile开始'+str(fileaddress[0])+'/'+str(isfak))
                thread.start()
            elif self.judgepath(fileaddress[0]) == 0:
                # 文件夹上传部分
                isfak = QMessageBox.question(self, "COS_uploader", "是否全部使用随机文件名？（建议图床使用）",
                                             QMessageBox.Yes | QMessageBox.No)
                g = os.walk(str(fileaddress[0]))
                for path, dir_list, file_list in g:
                    for file_name in file_list:
                        filepathall = str(fileaddress[0]) + "/" + file_name
                        self.statusbar.showMessage("当前上传" + filepathall)
                        logging.info('当前上传'+ str(filepathall))
                        thread = Thread(target=self.uploadfile,
                                        args=(filepathall, isfak))
                        logging.debug('子进程uploadfile开始' + str(filepathall) + '/' + str(isfak))
                        thread.start()
        else:
            QMessageBox.warning(self, "警告", "参数未加载")
            logging.info('警告：参数未加载')

if __name__ == "__main__":
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
