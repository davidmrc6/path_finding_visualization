from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtCore import pyqtProperty

class CustomGraphicsTextItem(QGraphicsTextItem):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self._opacity = 1.0
        self.setOpacity(self._opacity)

    def getOpacity(self) -> float:
        return self._opacity

    def setOpacity(self, value) -> None:
        self._opacity = value
        super().setOpacity(value)

    opacity = pyqtProperty(float, getOpacity, setOpacity)
