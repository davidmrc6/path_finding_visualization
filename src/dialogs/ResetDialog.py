"""
This module contains the ResetDialog class, which is a dialog that allows the user to select a reset option.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class ResetDialog(QDialog):
    """
    Class that represents the reset dialog.
    
    The dialog allows the user to select a reset option from the following:
        - Reset All Cells
        - Reset Checked/Path Cells
        - Reset Obstacle Cells

    Args:
        QDialog: The QDialog class is the base class of dialog windows.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Options")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        title = QLabel("Choose Reset Option:")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.allButton = QPushButton("Reset All Cells")
        self.allButton.clicked.connect(lambda: self.selectOption('all'))
        layout.addWidget(self.allButton)

        self.checkedPathButton = QPushButton("Reset Checked/Path Cells")
        self.checkedPathButton.clicked.connect(lambda: self.selectOption('checked_path'))
        layout.addWidget(self.checkedPathButton)

        self.obstacleButton = QPushButton("Reset Obstacle Cells")
        self.obstacleButton.clicked.connect(lambda: self.selectOption('obstacle'))
        layout.addWidget(self.obstacleButton)

        self.setLayout(layout)

    def selectOption(self, option: str):
        """
        Handle the reset option selection event.

        Args:
            option (str): the reset option selected by the user.
        """
        self.selectedOption = option
        self.accept()

    def getSelectedOption(self) -> str:
        """
        Get the selected reset option.

        Returns:
            str: the selected reset option.
        """
        return self.selectedOption
