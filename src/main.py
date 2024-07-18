""" 
Main module of the application. 

Adds the src directory to the system path, then
initializes the QApplication.

"""

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF 
from PyQt5.QtWidgets import QWidget

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from src.gui.GridWindow import GridWindow

def main() -> None:
    """ 
    Entry point of the application.
    
    Initializes the QApplication and the main window QWindow,
    then starts application event loop.
    
    Returns: 
        None

    """
    app = QApplication(sys.argv)

    window = GridWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
