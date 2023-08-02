import os
import time
import sys
import cv2
import threading
import requests
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore


class MyWidget(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setObjectName("MainWindow")
		self.setWindowTitle(' ')
		self.setStyleSheet('background: white;')
		self.resize(1500, 1100)

		self.screen = QDesktopWidget().screenGeometry()
		self.move(self.screen.width() * 30 // 100, self.screen.height() * 20 // 100)
		self.set_background('andrew.jpg')												# set background image

		self.num = 30 * 60																# initial time in seconds
		self.alarm = 'sample.mp3'
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.count)

		self.ui()																		# create the user interface elements

		self.GMT = datetime.timezone(datetime.timedelta(hours=8))						# set GMT timezone with +8 hours

		self.gesture_flag = True														# gesture flag
		video = threading.Thread(target = self.opencv)									# start video thread for gesture frame
		video.start()


	def ui(self):
		# Create UI elements here

		# timer cube
		self.btn_start = QtWidgets.QPushButton(self)
		self.btn_start.setText("00:00")
		self.btn_start.setGeometry((1500 - 350) // 2, 150, 350, 300)					# (x, y, width, height)
		self.btn_start.setStyleSheet('font-size: 100px; color:red; border: 1px solid black; background-color: rgba(0, 0, 0, 0.7); border-radius: 75px;')
		self.btn_start.clicked.connect(self.start)

		# home button
		self.btn_home = QtWidgets.QPushButton(self)
		self.btn_home.setText('home')
		self.btn_home.setGeometry(50, 50, 100, 100)										# (x, y, width, height)
		self.btn_home.setStyleSheet('background-color: rgba(255, 255, 255, 0.7); border-radius: 20px; font-weight: bold;')
		self.btn_home.clicked.connect(self.show_home)
		self.btn_home.hide()

		# switch button
		self.switch = QtWidgets.QPushButton(self)
		self.switch.setGeometry(50, 50, 100, 100)
		self.switch.setText('face')
		self.switch.setStyleSheet('background-color: rgba(255, 255, 255, 0.7); border-radius: 20px; font-weight: bold;')
		self.switch.clicked.connect(self.show_face)

		# gesture detection
		self.gesture = QtWidgets.QLabel(self)
		self.gesture.setGeometry(1000, 700, 400, 300)

		# face detection
		self.face = QtWidgets.QLabel(self)
		self.face.setGeometry(300, 100, 900, 800)
		self.face.setStyleSheet('background-color: rgba(255, 255, 255, 0.6); border-radius: 75px;')
		self.face.hide()


	def show_face(self):
		# Show face detection screen and hide other elements
		self.btn_start.hide()
		self.gesture.hide()
		self.switch.hide()
		self.btn_home.show()
		self.face.show()
		self.gesture_flag = False														# turn off camera for gesture


	def show_home(self):
		# Show home screen and hide face detection screen
		self.btn_start.show()
		self.gesture.show()
		self.switch.show()
		self.btn_home.hide()
		self.face.hide()

		self.gesture_flag = True														# turn on camera for gesture
		video = threading.Thread(target = self.opencv)
		video.start()


	def count(self):
		# Update timer display
		if time.time() < self.end_time:
			remaining_time = int(self.end_time - time.time())
			self.minutes, self.seconds = divmod(remaining_time, 60)

			self.btn_start.setText(f"{self.minutes:02d}:{self.seconds:02d}")
		else:
			 # Timer expired, play the alarm sound
			os.system('mpg123 ' + self.alarm)
			print("\nTime's up! Timer expired.")

			self.num = 5 * 60
			self.start()																# Start a rest timer


	def start(self):
		# Start the timer
		self.minutes, self.seconds = divmod(self.num, 60)
		self.start_time = time.time()
		self.end_time = self.start_time + self.num

		self.timer.start(1000)


	def opencv(self):
		# OpenCV video capture for gesture detection
		cap = cv2.VideoCapture(0)

		if not cap.isOpened():
			print('Cannot open camera')
			exit()

		while self.gesture_flag:
			# Capture video frame from camera
			ret, frame = cap.read()

			if not ret:
				print('Cannot receive frame')
				break

			frame = cv2.resize(frame, (400, 300))										# resize frame
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)								# convert to RBG
			height, width, channel = frame.shape										# get size and channel
			bytesPerline = channel * width												# calculate bytesPerline

			img = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)		# convert images to QImage, so that PyQt5 can read it.
			self.gesture.setPixmap(QPixmap.fromImage(img))								# display frame on QLabel.


	def set_background(self, image_path):
		# Set the window background image
		background_label = QLabel(self)
		background_label.setAlignment(Qt.AlignCenter)
		background_label.setGeometry(0, 0, self.width(), self.height())

		pixmap = QPixmap(image_path)  													# Load the image
		if not pixmap.isNull():
			background_label.setPixmap(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

		palette = self.palette()														# Set the window palette to the background color of the image
		palette.setBrush(QPalette.Background, QBrush(pixmap))
		self.setPalette(palette)


	def closeEvent(self, event):
		# automatically called by PyQt when the main window is closed.
		self.closeOpenCV()
		event.accept()


	def closeOpenCV(self):
		# Stop the gesture detection thread
		self.gesture_flag = False


	def clock(self):
		# Update window title with current time
		now = datetime.datetime.now(tz=self.GMT).strftime('%H:%M')
		self.setWindowTitle(now)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = MyWidget()
	MainWindow.show()

	# Start a QTimer to update the window title with the current time every 500 milliseconds
	clock = QtCore.QTimer()
	clock.timeout.connect(MainWindow.clock)
	clock.start(500)

	sys.exit(app.exec_())
