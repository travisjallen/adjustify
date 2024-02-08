"""
qt_main.py

Handles all GUI related tasks for adjustify.

Author: Travis Allen
02/24
"""

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from spotify_utils import SpotifyUtils
import threading

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        ## spotify setup
        self.spotify_utils = SpotifyUtils()
        self.sp = self.spotify_utils.client
        self.running = True

        self.hello = ["Hello World", "Hallo Welt", "Hola Mundo"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.button_click)

        ## artist skip
        self.skip_artist_checkbox = QtWidgets.QCheckBox(f'Skip Artists', None)
        self.layout.addWidget(self.skip_artist_checkbox)
        self.skip_artist_checkbox.stateChanged.connect(self.skip_artist_timer)


    @QtCore.Slot()
    def button_click(self):
        self.text.setText(random.choice(self.hello))


    @QtCore.Slot()
    def skip_artist_timer(self):
        if self.skip_artist_checkbox.isChecked():
            self.spotify_utils.artist_skip(self.sp,"Watchhouse")
            if self.running:
                self.t = threading.Timer(0.1, self.skip_artist_timer)
                self.t.start()

def appExec():
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800,600)
    widget.show()
    app.exec()
    
    ## kill the skip_artist_timer thread
    widget.running = False

if __name__ == '__main__':
    # app = QtWidgets.QApplication([])

    # widget = MyWidget()
    # widget.resize(800,600)
    # widget.show()

    # sys.exit(app.exec())
    sys.exit(appExec())