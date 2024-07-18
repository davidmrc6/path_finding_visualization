"""
This module contains the WindowEventHandler class which is responsible for handling events on the main window.

"""

import os
import threading

from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot

from src.dialogs.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from src.dialogs.ResetDialog import ResetDialog

class WindowEventHandler:
    """
    Class that handles events on the main window.
    """
    def __init__(self, grid_window):
        self.grid_window = grid_window
        self.lock = threading.Lock()

    def solverClicked(self) -> None:
        """
        Handle the solve button click event.
        
        This method is called when the user clicks the solve button. It
        first checks whether the start and end nodes are set on the grid,
        then shows the algorithm selection dialog. If the user selects an
        algorithm, it stops the current search and starts the selected algorithm.
        """
        # Print to console to check if method works as expected
        print("Solve button clicked!")
        
        # Checks if start and end nodes are set - if not, display an error message
        if not self.grid_window.gridWidget.getStartNodeState():
            QMessageBox.critical(self.grid_window, "Error", "Start node is not set.")
            return
        if not self.grid_window.gridWidget.getEndNodeState():
            QMessageBox.critical(self.grid_window, "Error", "End node is not set.")
            return
        
        # Show the algorithm selection dialog
        with self.lock:
            overlay = self.showBlurOverlay()
            dialog = AlgorithmSelectionDialog(self.grid_window)
            if dialog.exec_() == QDialog.Accepted:
                self.grid_window.stopCurrentSearch()
                selectedAlgorithm = dialog.getSelectedAlgorithm()
                
                self.grid_window.currentSearch = self.grid_window.algorithmToInstanceMap[selectedAlgorithm]
                    
                if self.grid_window.currentSearch:
                    self.grid_window.gridWidget.resetGrid('checked_path')
                    self.grid_window.currentSearch.startSearch()
                
            overlay.deleteLater()

        
    def resetClicked(self) -> None:
        """
        Handle the reset button click event.
        
        This method is called when the user clicks the reset button. It stops
        the current search and shows the reset dialog. If the user selects an
        option, it resets the grid accordingly.
        """
        print("Reset button clicked!")
        with self.lock:
            self.grid_window.stopCurrentSearch()
            
            overlay = self.showBlurOverlay()
            dialog = ResetDialog(self.grid_window)
            if dialog.exec_() == QDialog.Accepted:
                option = dialog.getSelectedOption()
                self.grid_window.gridWidget.resetGrid(option)
            overlay.deleteLater()
    
    def showBlurOverlay(self) -> QWidget:
        """
        Show a blur overlay on the main window.

        Returns:
            QWidget: the blur overlay widget.
        """
        overlay = QWidget(self.grid_window)
        overlay.setObjectName("blurOverlay")
        overlay.setGeometry(self.grid_window.rect())
        self.applyStylesheet(overlay, 'src/styles.qss')
        overlay.show()
        return overlay
        
    def applyStylesheet(self, widget, stylesheet_path) -> None:
        """
        Apply a stylesheet to a widget.

        Args:
            widget: The widget onto which the stylesheet is to be applied.
            stylesheet_path: The file path to the stylesheet (which is a .qss file).
        """
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r') as file:
                widget.setStyleSheet(file.read())
                
    def noPathFoundHandler(self):
        """
        Handle the no path found event.
        
        This method is called when the search algorithm does not find a path from
        the start node to the end node. In this case, it shows a warning message.
        """
        QMessageBox.warning(self.grid_window, "No Path Found", "There is no possible path from start to end.")

    def changeSpeed(self):
        """
        Handle the speed slider value change event.
        """
        speed = self.grid_window.speedSlider.value()
        for algorithm in self.grid_window.algorithmToInstanceMap.values():
            algorithm.setDelay(speed)
