from GoodNessMain import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QMenu
from PyQt5.QtCore import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import math

class CustomMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Worker = Worker1()
        self.Worker.start()
        self.Worker.ImageUpdate.connect(self.ImageUpdateSlot)
        # ----------------- Настройка для Serial Port ----------------- #
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        self.serial.readyRead.connect(self.onRead)  # Сигнал readyRead,которыйвызываетсякогдаSerialPort,что-тонаприёмку
        # ------------------------------------------------------------- #

        # ----- Добавляем список портов в ComboBox -------------------- #
        portList = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            portList.append(port.portName())
        self.comL.addItems(portList)

        # ----- Добавляем список портов в Settings > MenuPortList ----- #
        for i, port in enumerate(portList):
            comL = self.menuPortList.addAction(str(port))
            comL.triggered.connect(self.onOpen)
            if i >= 2:
                break
        # ------------------------------------------------------------- #
        self.actionOpenPort.triggered.connect(self.onOpen)
        self.actionClosePort.triggered.connect(self.onClose)
        self.actionReset.triggered.connect(self.onReset)
        # ------------------------------------------------------------- #
        self.speedSlider.valueChanged.connect(self.dSpeed)
        self.servoSlider.valueChanged.connect(self.dServo)
        self.ledC.stateChanged.connect(self.ledControl)
        self.QR_Forward.clicked.connect(self.dFORWARD)
        self.QR_Stop.clicked.connect(self.dSTOP)
        self.QR_Back.clicked.connect(self.dBACKWARD)

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

    def onOpen(self):
        self.serial.setPortName(self.comL.currentText())
        self.serial.open(QIODevice.ReadWrite)

    def onClose(self):
        self.serial.close()

    # --------Функция для получение данных через Serial > выводим полученные данные на дисплей-------- #
    def onRead(self):
        if not self.serial.canReadLine():
            return
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(',')
        if data[0] == '0':
            self.temperaturL01.display(data[1])
            self.temperaturL02.display(data[2])

    # ------------------------------------------------------------------------------------------------ #

    # --------Функция для отправки данных на Serial -------- #
    def serialSend(self, data):
        txs = ','.join(map(str, data)) + ';'
        self.serial.write(txs.encode())
        # 1. map(str, data) применяет функцию str к каждому элементу в списке data, преобразуя его в строковую форму.
        # 2. ','.join(...) объединяет преобразованные элементы списка data в одну строку, разделяя их запятой.
        # Результат этого шага будет строкой вида "элемент1,элемент2,элемент3".
        # 3. '+' конкатенирует полученную строку с символом ;. Результат будет строкой с добавленным символом ; в конце.
    # ------------------------------------------------------- #

    def ledControl(self, val):
        if val == 2: val = 1;
        self.serialSend([0, val])
        print(val)
    # ----------Ползунки---------- #
    def dSpeed(self, val):
        self.serialSend([1, self.speedSlider.value()])
        print(val)
    def dServo(self, val):
        self.serialSend([2, self.servoSlider.value()])
        print(val)
    # ---------------------------- #

    # ------------------Кнопки------------------ #
    def dFORWARD(self, val):
        self.serialSend([3])
    def dSTOP(self, val):
        self.serialSend([4])
    def dBACKWARD(self, val):
        self.serialSend([5])
    # ------------------------------------------ #
    def ImageUpdateSlot(self, Image):
        self.QTcamera.setPixmap(QPixmap.fromImage(Image))

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    # ControlXYUpdate = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.controlXY = 0
        print(f"Инициализация класса {self.__class__}")



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
                        controlXY = 100 * (cx - width / 2) / width
                        controlXY = controlXY * 1
                        cv2.drawContours(frame, maxcont, -1, (0, 255, 0), 2)
                        cv2.line(frame, (cx, 0), (cx, height), (0, 0, 255), 6)
                        cv2.line(frame, (0, cy), (width, cy), (0, 255, 0), 6)
                cv2.putText(frame, 'iSee: {};'.format(iSee), (width - 370, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(frame, 'controlX: {:.2f}'.format(controlXY), (width - 200, height - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
            ConvertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
            Pic = ConvertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)

            # --- Для отображение на QLabel --- #

    # def ContrColor(self):
    #     return self.controlXY

def stop(self):
    self.ThreadActive = False
    self.quit()

class SendColor(CustomMainWindow, Worker1):
#     def __init__(self):
#         super().__init__()
#     # def __init__(self, worker1_object):
#     #     super().__init__()  # Вызываем конструктор родительских классов
#     #     self.worker1 = worker1_object  # Сохраняем объект Worker1 в атрибуте класса SendColor
    pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    W = Worker1()
    print(f"Класс Worker имеет{W.__dict__}")
    mainWindow = CustomMainWindow()
    print(f"Класс CustomMainWindow имеет{mainWindow.__dict__}")
    print(issubclass(QThread, Ui_MainWindow)) #False
    print(issubclass(CustomMainWindow, Ui_MainWindow)) #True
    print(issubclass(Worker1, QThread)) #True
    print(issubclass(SendColor, Worker1)) #True SendColor наследуется атрибуты от Worker
    print(issubclass(SendColor, CustomMainWindow)) # True SendColor наследуется от CustomMainWindow
    print(issubclass(Worker1, CustomMainWindow)) # True SendColor наследуется от CustomMainWindow

    mainWindow.show()
    sys.exit(app.exec_())
