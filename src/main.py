import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from PyQt5.QtWidgets import QApplication
#from PyQt5.QtCore import Qt, QRectF

from src.gui.GridWindow import GridWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF 
from PyQt5.QtWidgets import QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GridWindow()
    window.show()
    sys.exit(app.exec_())