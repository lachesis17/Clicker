import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import pyautogui, time, random
from rich.console import Console

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.setWindowTitle("Clicker")
        self.setWindowIcon(QtGui.QIcon('mouse.svg'))
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.click_button.setIcon(QtGui.QIcon('mouse.svg'))
        self.click_button.setCheckable(True)
        self.click_button.clicked.connect(self.handle_click)

        self.worker = ThreadHandler()
        self.clicking_thread = Clicker()
        self.worker.func = self.clicking_thread.click_me
        self.worker.finished.connect(lambda: print("Thread finished"))
        self.clicking_thread.update_text.connect(self.update_display)

    def handle_click(self):
        if self.click_button.isChecked():
            self.clicking_thread._clicking = True
            print("Starting thread...")
            if not self.worker.isRunning():
                self.worker.start()
            self.click_button.setText("Stop Clicking")
        else:
            self.clicking_thread._clicking = False
            print("Stopping thread...")
            self.worker.quit()
            self.click_button.setText("Start Clicking")
            self.update_display(["Stopped"])

    def update_display(self, values):
        self.text_edit.clear()
        colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink', 'brown']
        for value in values:
            color = random.choice(colors)
            self.text_edit.setTextColor(QtGui.QColor(color))
            self.text_edit.setFontWeight(QtGui.QFont.Bold)
            self.text_edit.setAlignment(QtCore.Qt.AlignCenter)
            self.text_edit.append(str(value))

class Clicker(QtWidgets.QWidget):
    update_text = QtCore.pyqtSignal(list)
    _clicking = False

    def click_me(self):
        console = Console()
        history = ["oh yeah..."]
        console.log("Clicking process started")
        x = 0
        times = 8000
        self.update_text.emit(history)
        
        while x < times:
            pyautogui.click()
            time.sleep(3)
            x += 1
            history.append(x)
            self.update_text.emit(history[-7:])
            color = random.choice(['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink'])
            console.print(f'[{color}]{x}[/{color}]')
        self._clicking = False  # Ensure flag is reset when stopping
        print("Clicking ended...")

class ThreadHandler(QtCore.QThread):
    def __init__(self):
        super(ThreadHandler, self).__init__()
        self.func = None

    def run(self):
        if self.func:
            try:
                self.func()
            except Exception as e:
                print("Error in thread:", e)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    sys.excepthook = except_hook
    main()