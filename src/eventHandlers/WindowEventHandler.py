import os
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot

from src.dialogs.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from src.dialogs.ResetDialog import ResetDialog

class WindowEventHandler:
    def __init__(self, grid_window):
        self.grid_window = grid_window

    def solverClicked(self) -> None:
        print("Solve button clicked")
        
        if not self.grid_window.gridWidget.getStartNodeState():
            QMessageBox.critical(self.grid_window, "Error", "Start node is not set.")
            return
        if not self.grid_window.gridWidget.getEndNodeState():
            QMessageBox.critical(self.grid_window, "Error", "End node is not set.")
            return
        
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
        
        if self.grid_window.currentSearch and self.grid_window.currentSearch.search_thread.is_alive():
            self.grid_window.currentSearch.stopSearch()
        
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
