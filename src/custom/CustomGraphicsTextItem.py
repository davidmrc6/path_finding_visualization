"""
This module contains the CustomGraphicsTextItem class, which is a custom QGraphicsTextItem class that allows
for the setting of the opacity property.
"""

from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtCore import pyqtProperty

class CustomGraphicsTextItem(QGraphicsTextItem):
    """
    Class that represents a custom QGraphicsTextItem.
    
    The class allows for the setting of the opacity property.

    Args:
        QGraphicsTextItem: The QGraphicsTextItem class provides a text item that you can add to a QGraphicsScene to display formatted text.
    """
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self._opacity = 1.0
        self.setOpacity(self._opacity)

    def getOpacity(self) -> float:
        """
        Get the opacity property of the QGraphicsTextItem.

        Returns:
            float: the opacity property of the QGraphicsTextItem.
        """
        return self._opacity

    def setOpacity(self, value) -> None:
        """
        Set the opacity property of the QGraphicsTextItem.

        Args:
            value (float): the value to set the opacity property.
        """
        self._opacity = value
        super().setOpacity(value)

    # Define the opacity property
    opacity = pyqtProperty(float, getOpacity, setOpacity)
