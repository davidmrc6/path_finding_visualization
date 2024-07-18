# src/eventHandlers/WindowEventHandler.py

import os
from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtCore import pyqtSlot

from src.dialogs.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from src.dialogs.ResetDialog import ResetDialog

class WindowEventHandler:
    def __init__(self, grid_window):
        self.grid_window = grid_window

    def solverClicked(self) -> None:
        print("Solve button clicked")
        overlay = self.showBlurOverlay()
        dialog = AlgorithmSelectionDialog(self.grid_window)
        if dialog.exec_() == QDialog.Accepted:
            selectedAlgorithm = dialog.getSelectedAlgorithm()
            
            self.grid_window.currentSearch = self.grid_window.algorithmToInstanceMap[selectedAlgorithm]
                
            if self.grid_window.currentSearch:
                self.grid_window.gridWidget.resetGrid('checked_path')
                self.grid_window.currentSearch.startSearch()
            
        overlay.deleteLater()
        
    def resetClicked(self) -> None:
        overlay = self.showBlurOverlay()
        dialog = ResetDialog(self.grid_window)
        if dialog.exec_() == QDialog.Accepted:
            option = dialog.getSelectedOption()
            self.grid_window.gridWidget.resetGrid(option)
        overlay.deleteLater()
    
    def showBlurOverlay(self) -> QWidget:
        overlay = QWidget(self.grid_window)
        overlay.setObjectName("blurOverlay")
        overlay.setGeometry(self.grid_window.rect())
        self.applyStylesheet(overlay, 'src/styles.qss')
        overlay.show()
        return overlay
        
    @pyqtSlot()
    def closeEvent(self, event):
        if self.grid_window.currentSearch:
            self.grid_window.currentSearch.stopSearch()
        event.accept()
        
    def applyStylesheet(self, widget, stylesheet_path) -> None:
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r') as file:
                widget.setStyleSheet(file.read())
