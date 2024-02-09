from GoodNessMain import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import sys
import cv2


class CustomMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        "Инициализируем интерфейс класса Ui_mainWindow методом setupUi"
        self.Worker = Worker1()
        self.Worker.start()
        self.Worker.ImageUpdate.connect(self.ImageUpdateSlot)
        """
        Создаём экземпляр класса Worker1, сохраняем его в атрибуте Worker > Запускаем с помощью метода start() > 
        Сигнал ImageUpdate из объекта Worker1 соединяется с методом ImageUpdateSlot, что позволяет обновлять
        изображение в главном окне при получении новых данных от Worker1
        """
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)

        """
        Экземпляр класса QSerialPort, сохраняем в serial > устанавливается скорость передачи данных
        """

        self.serial.readyRead.connect(self.onRead)
        self.serial.errorOccurred.connect(self.onReset)
        self.serial.aboutToClose.connect(self.onReset)

        portList = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            portList.append(port.portName())
        self.comL.addItems(portList)
        for i, port in enumerate(portList):
            comL = self.menuPortList.addAction(str(port))
            comL.triggered.connect(self.onOpen)
            if i >= 2:
                break
        self.actionOpenPort.triggered.connect(self.onOpen)
        self.actionClosePort.triggered.connect(self.onClose)
        self.actionReset.triggered.connect(self.onReset)
        # ------------------------- SerialPort ------------------------- #

        self.speedSlider.valueChanged.connect(self.dSpeed)
        self.servoSlider.valueChanged.connect(self.dServo)
        self.ledC.stateChanged.connect(self.ledControl)
        self.QR_Forward.clicked.connect(self.dFORWARD)
        self.QR_Stop.clicked.connect(self.dSTOP)
        self.QR_Back.clicked.connect(self.dBACKWARD)
        self.Worker.Run2(self.serialSend)  # По идее должна работать 1 2
        # self.serialSend(self.Worker.Run2)                 #По идее должна работать 2 1

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

    def dServo(self, val):
        self.serialSend([2, self.servoSlider.value()])

    def dFORWARD(self, val):
        self.serialSend([3, int(val)])

    def dSTOP(self, val):
        self.serialSend([4, int(val)])

    def dBACKWARD(self, val):
        self.serialSend([5, int(val)])

    def ImageUpdateSlot(self, Image):
        self.QTcamera.setPixmap(QPixmap.fromImage(Image))



class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.ThreadActive = False

    def Run2(self, val):
        print("Функция получила значения и начала работать", val)
        return val

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        if Capture.isOpened():
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
                    cv2.putText(frame, 'iSee: {};'.format(iSee), (width - 370, height - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.4,
                                (255, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, 'controlX: {:.2f}'.format(controlXY), (width - 200, height - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
                    if iSee == True:
                        val = [2, int(controlXY)]
                        self.Run2(val)
                        pass
                ConvertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
                Pic = ConvertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        else:
            Capture = self.find_camera()
            while Capture is None:  # Цикл поиска камеры
                Capture =  self.find_camera()()
            while self.ThreadActive:  # Начало трансляции после обнаружения камеры
                success, frame = Capture.read()
                if success:
                    height, width = frame.shape[0:2]
                    # Далее продолжайте обработку изображения как в предыдущем цикле

    def find_camera(self):
        while True:
            Capture = cv2.VideoCapture(0)
            if Capture.isOpened():
                print("Камера найдена")
                return Capture
            else:
                print("Камера не найдена. Продолжить поиск?")
                key = cv2.waitKey(0)
                if key == 27:  # Нажатие клавиши Esc
                    break


def stop(self):
    self.ThreadActive = False
    self.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    print(f"Класс Worker имеет{Worker1.__dict__}")
    print(f"Класс CustomMainWindow имеет{CustomMainWindow.__dict__}")
    mainWindow = CustomMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
