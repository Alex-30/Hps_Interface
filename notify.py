import requests

from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
import sys, cv2, threading

app = QtWidgets.QApplication(sys.argv)
window_w, window_h = 900, 900

Form = QtWidgets.QWidget()
Form.setWindowTitle('notify')
Form.resize(window_w, window_h)

def windowResize(self):
    global window_w, window_h
    window_w = Form.width()
    window_h = Form.height()
    label.setGeometry(0,0,window_w,window_h)

Form.resizeEvent = windowResize

ocv = True
def closeOpenCV(self):
    global ocv
    ocv = False

Form.closeEvent = closeOpenCV

label = QtWidgets.QLabel(Form)
label.setGeometry(0,0,window_w,window_h - 100)

photo = False
def takePhoto():
    global photo
    photo = True

btn = QtWidgets.QPushButton(Form)
btn.setGeometry(0, 0, 100, 50)
btn.setText('photo')
btn.clicked.connect(takePhoto)

def opencv():
    global window_w, window_h, ocv, photo
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while ocv:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        if photo == True:
            photo = False
            cv2.imwrite('selfie.jpg', frame)

            url = 'https://notify-api.line.me/api/notify'
            token = 'fZ8GSExATGmYiD7lR7buL2GtRUPPBGizqYArfpwsXwX'

            headers = { 'Authorization': 'Bearer ' + token }
            data = { 'message': 'testing!' }
            files = { 'imageFile': ('selfie.jpg', open('selfie.jpg', 'rb'), 'image/jpeg') }

            data = requests.post(url, headers=headers, data=data, files=files)

        frame = cv2.resize(frame, (window_w, window_h - 100))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytesPerline = channel * width
        img = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(img))

video = threading.Thread(target=opencv)
video.start()

Form.show()
sys.exit(app.exec_())



