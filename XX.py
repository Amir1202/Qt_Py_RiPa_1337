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

        # ------------------------- Serial ------------------------- #
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        """
        Экземпляр класса QSerialPort, сохраняем в serial > устанавливается скорость передачи данных
        """

        self.serial.readyRead.connect(self.onRead)
        """
        Генерируется сигнал, когда есть данные для чтения от МК, и отправляются в метод onRead,
        дальше он обрабатывается
        """

        portList = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            portList.append(port.portName())
        self.comL.addItems(portList)
        for i, port in enumerate(portList):
            comL = self.menuPortList.addAction(str(port))
            comL.triggered.connect(self.onOpen)

        """
        1. Создается пустой список portList.
        2. Получаем список доступных портов с помощью QSerialPortInfo().availablePorts().
        3. Для каждого порта в списке ports, имя порта добавляется в список portList.
        4. Создается выпадающее меню comL, которое заполняется элементами из списка portList.
        5. Для каждого элемента в списке portList, создается действие comL в меню
         self.menuPortList, и связывается с методом self.onOpen().
        """

        self.actionOpenPort.triggered.connect(self.onOpen)
        self.actionClosePort.triggered.connect(self.onClose)
        self.actionReset.triggered.connect(self.onReset)

        """
        Методы для МенюБар'а, связь кнопок с методами для их обработки
        """
        # ------------------------- Serial ------------------------- #

        self.speedSlider.valueChanged.connect(self.dSpeed)
        self.servoSlider.valueChanged.connect(self.dServo)
        self.ledC.stateChanged.connect(self.ledControl)
        self.QR_Forward.clicked.connect(self.dFORWARD)
        self.QR_Stop.clicked.connect(self.dSTOP)
        self.QR_Back.clicked.connect(self.dBACKWARD)

        """
        Методы для кнопок, связь кнопок с методами для их обработки
        """
        # self.Worker.Run2(self.serialSend)  # По идее должна работать 1 2
        # self.serialSend(self.Worker.Run2)  #По идее должна работать 2 1

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
    # --------Метод для чтения данных от Serial -------- #
    def onRead(self):
        if not self.serial.canReadLine(): return
        rx = self.serial.readLine()
        data = str(rx, 'utf-8').strip().split(',')
        # парсинг
        if data[0] == '0':
            self.temperaturL01.display(data[1])
            self.temperaturL02.display(data[2])
        elif data[0] == '1':
            print(data[1])
        elif data[0] == '2':
            print(data[1])
    """
    1. Проверяется, есть ли что-то, что может быть прочитано из серийного порта.
    2. Если нечего читать, то выходим
    4. Прочитанная строка декодируется из байтов в строку с использованием кодировки 'utf-8' и удаляются
     начальные и конечные пробелы.
    5. Декодированная строка разделяется на подстроки, разделенные запятыми, с помощью метода split(',').
    """
    # --------Метод для отправки данных на Serial -------- #
    def serialSend(self, data):
        txs = ','.join(map(str, data)) + ';'
        self.serial.write(txs.encode()) # преобразовать в байты и отправить
        """        
        1. map(str, data) применяет функцию str к каждому элементу в списке data, преобразуя его в строковую форму.
        2. ','.join(...) объединяет преобразованные элементы списка data в одну строку, разделяя их запятой.
        Результат этого шага будет строкой вида "элемент1,элемент2,элемент3".
        3. '+' конкатенирует полученную строку с символом ;. Результат будет строкой с добавленным символом ; в конце.
        """
    # ------------------------------------------------------- #

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
        if Image is not None:
            self.QTcamera.setPixmap(QPixmap.fromImage(Image))
        else:
            self.QTcamera.setPixmap(QPixmap.fromImage(Image))

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.ThreadActive = False
        self.MainMain = CustomMainWindow
    def Run2(self, val):
        print("Функция получила значения и начала работать", val)
        # self.MainMain.serialSend(val)
        return val
    def find_camera(self):
        # Проверка наличия камеры
        Capture = cv2.VideoCapture(0)
        success = Capture.isOpened()
        Capture.release()
        print(f"Камера подключена {success}")
        return success
    def run(self):
        self.ThreadActive = True
        camera_found = self.find_camera()
        while not camera_found and self.ThreadActive:
            camera_found = self.find_camera()
        while self.ThreadActive:
            try:
                Capture = cv2.VideoCapture(0)
                while True:
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
                        cv2.putText(frame, 'iSee: {};'.format(iSee), (width - 370, height - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                    (255, 0, 0), 1, cv2.LINE_AA)
                        cv2.putText(frame, 'controlX: {:.2f}'.format(controlXY), (width - 200, height - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
                    ConvertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
                    Pic = ConvertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)
            except:
                print("Камера была отключена. Повторный поиск камеры.")
                while self.ThreadActive:
                    self.run()
def stop(self):
    self.ThreadActive = False
    self.quit()

if __name__ == "__main__":
    print(f"Класс Worker имеет{Worker1.__dict__}")
    print(f"Класс CustomMainWindow имеет{CustomMainWindow.__dict__}")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CustomMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
