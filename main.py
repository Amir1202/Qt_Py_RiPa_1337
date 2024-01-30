from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QMenu
from PyQt5.QtCore import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import math

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 665)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.QTcamera = QtWidgets.QLabel(self.centralwidget)
        self.QTcamera.setStyleSheet("\n"
"QLabel{\n"
"border: 2px solid rgb(0, 85, 127);\n"
"border-radius: 4px;\n"
"padding: 2px;\n"
"background-color:rgb(37, 37, 56);\n"
"color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(255, 194, 0, 255), stop:1 rgba(255, 238, 97, 252));\n"
"font: 16pt \"Impact\";\n"
"}")
        self.QTcamera.setAlignment(QtCore.Qt.AlignCenter)
        self.QTcamera.setObjectName("QTcamera")
        self.horizontalLayout.addWidget(self.QTcamera)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lcdNumber_8 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_8.setMaximumSize(QtCore.QSize(16777215, 1200))
        self.lcdNumber_8.setStyleSheet("\n"
"QLCDNumber{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"stop:0.0284091 rgba(255, 0, 79, 255), stop:1 rgba(255, 124, 55, 252)); color: rgb(255, 255, 255);}")
        self.lcdNumber_8.setObjectName("lcdNumber_8")
        self.verticalLayout_2.addWidget(self.lcdNumber_8)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 10, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.QR_Forward = QtWidgets.QRadioButton(self.centralwidget)
        self.QR_Forward.setMaximumSize(QtCore.QSize(60, 13))
        self.QR_Forward.setObjectName("QR_Forward")
        self.verticalLayout_3.addWidget(self.QR_Forward)
        self.QR_Stop = QtWidgets.QRadioButton(self.centralwidget)
        self.QR_Stop.setMaximumSize(QtCore.QSize(60, 13))
        self.QR_Stop.setObjectName("QR_Stop")
        self.verticalLayout_3.addWidget(self.QR_Stop)
        self.QR_Back = QtWidgets.QRadioButton(self.centralwidget)
        self.QR_Back.setMaximumSize(QtCore.QSize(60, 13))
        self.QR_Back.setObjectName("QR_Back")
        self.verticalLayout_3.addWidget(self.QR_Back)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.speedSlider = QtWidgets.QSlider(self.centralwidget)
        self.speedSlider.setStyleSheet("QSlider::groove:vertical { background: blue; position: absolute; left: 0px; right: 0px; border-radius: 4px;}\n"
"QSlider::handle:vertical {\n"
"background:#880000;\n"
"width: 12px;\n"
"margin: -10px -10px;\n"
"}\n"
"QSlider::add-page:vertical { background: red;}\n"
"QSlider::sub-page:vertical {background: white;}")
        self.speedSlider.setMinimum(800)
        self.speedSlider.setMaximum(1700)
        self.speedSlider.setPageStep(1)
        self.speedSlider.setProperty("value", 1450)
        self.speedSlider.setOrientation(QtCore.Qt.Vertical)
        self.speedSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.speedSlider.setTickInterval(100)
        self.speedSlider.setObjectName("speedSlider")
        self.horizontalLayout_5.addWidget(self.speedSlider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 30, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.servoSlider = QtWidgets.QSlider(self.centralwidget)
        self.servoSlider.setStyleSheet("\n"
"QSlider::groove:horizontal {background: white; position: absolute; left: 10px; right: 10px;}\n"
"QSlider::handle:horizontal {height: 10px; background: black; margin: 0 -10px; /* расширяется наружу от бороздки */ }")
        self.servoSlider.setMaximum(180)
        self.servoSlider.setPageStep(1)
        self.servoSlider.setSliderPosition(90)
        self.servoSlider.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider.setObjectName("servoSlider")
        self.horizontalLayout_4.addWidget(self.servoSlider)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(5, 30, 5, 30)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lcdNumber_7 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_7.setStyleSheet("\n"
"QLCDNumber{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"stop:0.0284091 rgba(255, 0, 79, 255), stop:1 rgba(255, 124, 55, 252)); color: rgb(255, 255, 255);}")
        self.lcdNumber_7.setObjectName("lcdNumber_7")
        self.verticalLayout_9.addWidget(self.lcdNumber_7)
        self.horizontalLayout_4.addLayout(self.verticalLayout_9)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.comL = QtWidgets.QComboBox(self.centralwidget)
        self.comL.setMaximumSize(QtCore.QSize(60, 20))
        self.comL.setObjectName("comL")
        self.verticalLayout_4.addWidget(self.comL)
        self.ledC = QtWidgets.QCheckBox(self.centralwidget)
        self.ledC.setMaximumSize(QtCore.QSize(16, 16))
        self.ledC.setText("")
        self.ledC.setObjectName("ledC")
        self.verticalLayout_4.addWidget(self.ledC)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.TextTemp = QtWidgets.QLabel(self.centralwidget)
        self.TextTemp.setStyleSheet("\n"
"font: 8pt \"Portico Light\";\n"
"color: rgb(0, 85, 255);")
        self.TextTemp.setObjectName("TextTemp")
        self.verticalLayout_7.addWidget(self.TextTemp)
        self.temperaturL01 = QtWidgets.QLCDNumber(self.centralwidget)
        self.temperaturL01.setObjectName("temperaturL01")
        self.verticalLayout_7.addWidget(self.temperaturL01)
        self.temperaturL02 = QtWidgets.QLCDNumber(self.centralwidget)
        self.temperaturL02.setObjectName("temperaturL02")
        self.verticalLayout_7.addWidget(self.temperaturL02)
        self.temperaturL03 = QtWidgets.QLCDNumber(self.centralwidget)
        self.temperaturL03.setObjectName("temperaturL03")
        self.verticalLayout_7.addWidget(self.temperaturL03)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.TextBLara = QtWidgets.QLabel(self.centralwidget)
        self.TextBLara.setStyleSheet("\n"
"font: 8pt \"Portico Light\";\n"
"color: rgb(0, 85, 255);")
        self.TextBLara.setObjectName("TextBLara")
        self.verticalLayout_8.addWidget(self.TextBLara)
        self.wetL01 = QtWidgets.QLCDNumber(self.centralwidget)
        self.wetL01.setObjectName("wetL01")
        self.verticalLayout_8.addWidget(self.wetL01)
        self.wetL02 = QtWidgets.QLCDNumber(self.centralwidget)
        self.wetL02.setObjectName("wetL02")
        self.verticalLayout_8.addWidget(self.wetL02)
        self.wetL03 = QtWidgets.QLCDNumber(self.centralwidget)
        self.wetL03.setObjectName("wetL03")
        self.verticalLayout_8.addWidget(self.wetL03)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1081, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuPortList = QtWidgets.QMenu(self.menuSetting)
        self.menuPortList.setObjectName("menuPortList")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpenPort = QtWidgets.QAction(MainWindow)
        self.actionOpenPort.setObjectName("actionOpenPort")
        self.actionClosePort = QtWidgets.QAction(MainWindow)
        self.actionClosePort.setObjectName("actionClosePort")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.menuPortList.addSeparator()
        self.menuSetting.addAction(self.menuPortList.menuAction())
        self.menuSetting.addAction(self.actionOpenPort)
        self.menuSetting.addAction(self.actionClosePort)
        self.menuSetting.addSeparator()
        self.menuSetting.addAction(self.actionReset)
        self.menuBar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)
        self.servoSlider.valueChanged['int'].connect(self.lcdNumber_7.display) # type: ignore
        self.speedSlider.valueChanged['int'].connect(self.lcdNumber_8.display) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.QTcamera.setText(_translate("MainWindow", "Загрузка..."))
        self.QR_Forward.setText(_translate("MainWindow", "Вперёд"))
        self.QR_Stop.setText(_translate("MainWindow", "СТОП"))
        self.QR_Back.setText(_translate("MainWindow", "Назад"))
        self.TextTemp.setText(_translate("MainWindow", "Температура"))
        self.TextBLara.setText(_translate("MainWindow", "Влажность"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.menuPortList.setTitle(_translate("MainWindow", "PortList"))
        self.actionOpenPort.setText(_translate("MainWindow", "OpenPort"))
        self.actionClosePort.setText(_translate("MainWindow", "ClosePort"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))

# ____________________________________________________Для того, чтобы всё работало____________________________________________________#
#         from PyQt5.QtGui import *
#         from PyQt5.QtWidgets import *
#         from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QMenu
#         from PyQt5.QtCore import *
#         import cv2
#         from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
#         from PyQt5 import QtCore, QtGui, QtWidgets

# ----------------- Настройка для Serial Port ----------------- #

        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        self.serial.readyRead.connect(self.onRead)  #Сигнал readyRead, который вызывается когда SerialPort, что-то на приёмку.

# ----------------- Настройка для Serial Port ----------------- #

        # ----- Добавляем список портов в ComboBox ----- #
        portList = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            portList.append(port.portName())
        self.comL.addItems(portList)
        # ---------------------------------------------- #

        # ----- Добавляем список портов в Settings > MenuPortList ----- #
        for i, port in enumerate(portList):
            comL = self.menuPortList.addAction(str(port))
            comL.triggered.connect(self.onOpen)
            if i >= 2:
                break

        self.actionOpenPort.triggered.connect(self.onOpen)
        self.actionClosePort.triggered.connect(self.onClose)
        self.actionReset.triggered.connect(self.onReset)
        # ---------------------------------------------- #

        self.speedSlider.valueChanged.connect(self.dSpeed)
        self.servoSlider.valueChanged.connect(self.dServo)
        self.ledC.stateChanged.connect(self.ledControl)

        self.QR_Forward.clicked.connect(self.dFORWARD)
        self.QR_Stop.clicked.connect(self.dSTOP)
        self.QR_Back.clicked.connect(self.dBACKWARD)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)



    def onReset(self):
        portlist = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            portlist.append(port.portName())
        self.comL.clear()
        self.comL.addItems(portlist)
        self.menuPortList.clear()
        for i, port in enumerate(portlist):
            comL = self.menuPortList.addAction(str(port))
            comL.triggered.connect(self.onOpen)
            if i >= 2:
                break

    def onOpen(self):
        self.serial.setPortName(self.comL.currentText())
        self.serial.open(QIODevice.ReadWrite)
    def onClose(self):
        self.serial.close()
    def onRead(self):
        if not self.serial.canReadLine():
            return
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(',')
        if data[0] == '0':
            self.temperaturL01.display(data[1])
            self.temperaturL02.display(data[2])
    def serialSend(self, data):
        txs = ""
        for val in data:
            txs += str(val)
            txs += ','
        txs = txs[:-1]
        txs += ';'
        self.serial.write(txs.encode())
    def ledControl(self, val):
        if val == 2: val = 1;
        self.serialSend([0, val])
    def dSpeed(self, val):
        self.serialSend([1, self.speedSlider.value()])
        print(val)
    def dServo(self, val):
        self.serialSend([2, self.servoSlider.value()])
        print(val)

# ----------------------------Кнопки---------------------------- #

    def dFORWARD(self, val):
        self.serialSend([3])
    def dSTOP(self, val):
        self.serialSend([4])
    def dBACKWARD(self, val):
        self.serialSend([5])

# ----------------------------Кнопки---------------------------- #

    def ImageUpdateSlot(self, Image):
        self.QTcamera.setPixmap(QPixmap.fromImage(Image))


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)

        while self.ThreadActive:
            iSee = False
            controlXY = 0
            success, frame = Capture.read()
            if success:
                height, width = frame.shape[0:2]
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                binary = cv2.inRange(hsv, (0, 100, 250), (20, 255, 255))

                roi = cv2.bitwise_and(frame, frame, mask=binary)
                contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                if len(contours) != 0:
                    maxcont = max(contours, key=cv2.contourArea)
                    moments = cv2.moments(maxcont)
                    if moments["m00"] > 20:
                        cx = int(moments["m10"] / moments["m00"])
                        cy = int(moments["m01"] / moments["m00"])
                        iSee = True
                        controlXY = 510 * (cx - width / 2) / width
                        controlXY = controlXY * 1
                        cv2.drawContours(frame, maxcont, -1, (0, 255, 0), 2)
                        cv2.line(frame, (cx, 0), (cx, height), (0, 0, 255), 6)
                        cv2.line(frame, (0, cy), (width, cy), (0, 255, 0), 6)
                cv2.putText(frame, 'iSee: {};'.format(iSee), (width - 370, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(frame, 'controlX: {:.2f}'.format(controlXY), (width - 200, height - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
                controlXY = int(controlXY)
                # print(controlXY)
                # controlXY = str((list(map(abs, controlXY))))
                # controlXY = contorlXY.replace("[", "").replace("]", "")



                def ControlServo_Color(self, controlXY):
                    if iSee == True:
                        self.main_window.serialSend([2, controlXY])
                    print(controlXY)





                # def ControlServo_Color(controlXY):
                #     if iSee == True:
                #         self.serialSend([2, controlXY])
                #     print(controlXY)

                # --- Для отображение на QLabel --- #

                ConvertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
                Pic = ConvertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

                # --- Для отображение на QLabel --- #



# -----Без выделение цветов----- #

        # while self.ThreadActive:
        #     ret, frame = Capture.read()
        #     if ret:
        #         Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        #         Pic = ConvertToQtFormat.scaled(1200, 800, Qt.KeepAspectRatio)
        #         self.ImageUpdate.emit(Pic)

# -----Без выделение цветов----- #


    def stop(self):
        self.ThreadActive = False
        self.quit()
    # ____________________________________________________Для того, чтобы всё работало____________________________________________________#

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
