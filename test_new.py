from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import sys, time

class ProgressBarThread(QThread):
    change_value =  Signal(int)
    thread_finished = Signal(int)

    def run(self):
        count = 0
        while count < 100:
            count += 1
            time.sleep(0.01)
            self.change_value.emit(count)
        
        self.thread_finished.emit(1)
    
    def stop(self):
        self.is_running = False
        print("Stopping Thread..")
        self.terminate()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread")
        self.setGeometry(100,100,200,200)
        self.show()
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        vbox = QVBoxLayout()
        self.widget.setLayout(vbox)

        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(100)
        vbox.addWidget(self.progressbar)
        
        self.button = QPushButton("Run")
        self.button.clicked.connect(self.start_progressbar)
        vbox.addWidget(self.button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_progressbar)
        vbox.addWidget(self.stop_button)
        self.stop_button.setDisabled(True)

    def start_progressbar(self):
        self.button.setDisabled(True)
        self.stop_button.setDisabled(False)
        self.thread = ProgressBarThread()
        self.thread.change_value.connect(self.set_progress_val)
        self.thread.thread_finished.connect(self.done_progressbar)
        self.thread.start()

    def set_progress_val(self, val):
        self.progressbar.setValue(val)

    def stop_progressbar(self):
        if self.thread:
            self.thread.stop()
            self.done_progressbar()

    def done_progressbar(self):
        self.button.setDisabled(False)
        self.stop_button.setDisabled(True)

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = Window()
sys.exit(app.exec())