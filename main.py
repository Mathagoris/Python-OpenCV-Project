import sys
from os import listdir
import thread
import ClimbingWallRouteDetection as routeFinder
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import *

class MainWindow(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setWindowTitle('Climbing Wall Route Detection')
		# x, y, width, height
		self.setGeometry(300, 150, 500, 500)
	
		# Container
		widget = QWidget()
		layout = QtGui.QGridLayout(self)

		# Add all images as buttons
		files = listdir('walls')
		for file in files:
			if file.endswith('.jpg'):
				self.addImageButton(layout, file)

		widget.setLayout(layout)

		# Scroll area
		scroll = QScrollArea()
		scroll.setWidgetResizable(False)
		scroll.setWidget(widget)

		vLayout = QVBoxLayout(self)
		vLayout.addWidget(scroll)
		self.setLayout(vLayout)
		self.show()

	def addImageButton(self, layout, file):
		button = QtGui.QPushButton(self)
		button.clicked.connect(lambda: self.findRoutes('walls/' + file))
		button.setIcon(QtGui.QIcon('walls/' + file))
		button.setIconSize(QtCore.QSize(200, 200))
		layout.addWidget(button)
	
	def findRoutes(self, file):
		# thread.start_new_thread(routeFinder.find_routes, ('walls/wall.jpg', ))
		# print("in new thread")
		routeFinder.find_routes(file)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())

