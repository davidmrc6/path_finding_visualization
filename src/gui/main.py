import sys
from PyQt5.QtWidgets import QApplication
#from PyQt5.QtCore import Qt, QRectF

from GridWindow import GridWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GridWindow()
    window.show()
    sys.exit(app.exec_())