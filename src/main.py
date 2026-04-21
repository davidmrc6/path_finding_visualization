""" 
Main module of the application. 

Adds the src directory to the system path, then
initializes the QApplication.

"""

import sys
import os

from PyQt5.QtWidgets import QApplication

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

    # Apply global stylesheet
    stylesheet_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, 'r') as file:
            app.setStyleSheet(file.read())

    window = GridWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
