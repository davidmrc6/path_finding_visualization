from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRectF, Qt

class Cell(QGraphicsRectItem):
    stateColorMap = {
        'empty': QColor(255, 255, 255),
        'obstacle': QColor(255, 0, 0),
        'checked': QColor(0, 255, 0),
        'start': QColor(0, 0, 255),
        'end': QColor(255, 255, 0),
        'path': QColor(255, 0, 255)
    }
    def __init__(self, x, y, size) -> None:
        super().__init__(0, 0, size, size)
        self.setPos(x * size, y * size)
        self.state = 'empty'
        self.updateColor()

    def updateColor(self) -> None:
        color = self.stateColorMap.get(self.state, QColor(255, 255, 255))
        self.setBrush(QBrush(color))
        
    def setState(self, state) -> None:
        self.state = state
        self.updateColor()