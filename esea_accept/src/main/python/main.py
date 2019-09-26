from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import (
    Qt,
    QThread,
    QCoreApplication,
    QTimer,
    pyqtSignal,
    QPropertyAnimation,
    QEasingCurve,
)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
    QRadioButton,
    QButtonGroup,
    QSpinBox,
    QProgressBar,
    QCheckBox,
    QMessageBox,
)

import sys
from esea_accept.reactor import *


def main():
    appctxt = ApplicationContext()
    template_path = appctxt.get_resource("argus.png")
    appctxt.app.setStyle("Fusion")
    window = MainWindow(template_path)
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
    return exit_code


class MainWindow(QWidget):
    def __init__(self, template_path):
        super().__init__()
        self.layout = QVBoxLayout()
        self.create_run_button()
        self.template_path = template_path

        # Window settings
        self.setLayout(self.layout)
        self.setFixedSize(150, 100)

    def create_run_button(self):
        self.run_button = QPushButton("Run!")
        self.run_button.clicked.connect(self.run)
        self.layout.addWidget(self.run_button)
        self.layout.setAlignment(self.run_button, Qt.AlignHCenter)

    def run(self):
        react(self.template_path)


if __name__ == "__main__":
    sys.exit(main())
