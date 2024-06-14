import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import pyautogui, time, ctypes
from rich.console import Console

ctypes.windll.shcore.SetProcessDpiAwareness(1)
appid = 'Clicker'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

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
        self.clicking_thread.update_text.connect(lambda x: self.update_display(x))

        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.click_button)
        self.click_button.setGraphicsEffect(self.opacity_effect)

        self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.6)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Linear)

        # Connect hover events
        self.click_button.installEventFilter(self)

    def eventFilter(self, object, event):
        if object == self.click_button:
            if event.type() == QtCore.QEvent.Enter:
                # Fade out on hover
                self.animation.setDirection(QtCore.QPropertyAnimation.Forward)
                self.animation.start()
            elif event.type() == QtCore.QEvent.Leave:
                # Fade in on hover leave
                self.animation.setDirection(QtCore.QPropertyAnimation.Backward)
                self.animation.start()
        return super().eventFilter(object, event)

    def handle_click(self):
        if self.click_button.isChecked():
            self.clicking_thread.keep_running = True
            if not self.worker.isRunning():
                self.worker.start()
        else:
            self.clicking_thread.keep_running = False
            self.worker.quit()
            self.update_display(["❌"])

    def update_display(self, values):
        self.text_edit.clear()
        colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink', 'brown']
        color_index = self.clicking_thread.counter 

        for value in values:
            color = colors[color_index % len(colors)]
            self.text_edit.setTextColor(QtGui.QColor(color))
            self.text_edit.setFontWeight(QtGui.QFont.Bold)
            self.text_edit.setAlignment(QtCore.Qt.AlignCenter)
            self.text_edit.append(str(value))
            color_index += 1

class Clicker(QtWidgets.QWidget):
    update_text = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.keep_running = False

    def click_me(self):
        console = Console()
        self.counter = 0
        history = ["🐭"]
        self.update_text.emit(history)
        colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink']

        while self.keep_running:
            time.sleep(2)
            pyautogui.click()
            self.counter += 1
            history.append(self.counter)
            color = colors[self.counter % len(colors)]
            console.print(f'[{color}]{self.counter}[/{color}]')
            if self.keep_running:
                self.update_text.emit(history[-10:])
        self.update_text.emit(["🌈"])

class ThreadHandler(QtCore.QThread):
    def __init__(self):
        super().__init__()
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
