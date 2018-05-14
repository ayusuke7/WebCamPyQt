import sys
import cv2

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUi


class CaptureDevice(QDialog):
    def __init__(self):
        super(CaptureDevice, self).__init__()
        loadUi('ui-interfaces\\CaptureDevice.ui', self)

        # Variaveis
        self.timer = QTimer(self)
        self.imagem = None

        # Declara Buttons
        self.btnCam.clicked.connect(self.start_stop_webcam)
        self.btnLoad.clicked.connect(self.load_video)

    def load_video(self):

        if self.timer.isActive() == True:
            self.timer.stop()
            self.btnCam.setText("START CAM")

        fileName, filter = QFileDialog.getOpenFileName(self,
         "Selecione um Video", "", "Arquivos de Video (*.mp4 *.avi *.mkv)")

        if fileName:
            self.capture = cv2.VideoCapture(fileName)
            self.start_time()

    def start_stop_webcam(self):

        if self.btnCam.text() == "START CAM":
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.start_time()
            self.btnCam.setText("STOP CAM")
        else:
            self.btnCam.setText("START CAM")
            self.timer.stop()

    def start_time(self):
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        
        ret, self.imagem = self.capture.read()
        if ret == True:

            if self.checkEixoX.isChecked():
                self.limited_area()

            self.set_display_image(self.imagem)

    def set_display_image(self, frame, label=1):

        qtimg = QImage.Format_Indexed8

        if len(frame.shape) == 3:  # rows, cols, chanels
            if (frame.shape[2]) == 4:  # chanels == RGBA
                qtimg = QImage.Format_RGBA888
            else:
                qtimg = QImage.Format_RGB888

        tmp = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0],
                     qtimg)
        tmp = tmp.rgbSwapped()

        if label == 1:
            self.lbFrames.setPixmap(QPixmap.fromImage(tmp))
            self.lbFrames.setScaledContents(True)

    def limited_area(self):

        # limite horizontal
        lmt = self.spinerX.value()
        cv2.line(self.imagem, (0, lmt), (self.imagem.shape[1], lmt), (0, 255, 255), 2)

        #shape = (larg=480, alt=640, 3)
        #cv2.rectangle(self.imagem, (200, 0), (0, 200), (0, 0, 255), 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CaptureDevice()
    janela.show()
    sys.exit(app.exec_())