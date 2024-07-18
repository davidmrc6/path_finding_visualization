from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt

class Cell(QGraphicsRectItem):
    stateColorMap = {
        'empty': QColor(245, 245, 245),
        'obstacle': QColor(102, 102, 102),
        'checked': QColor(198, 198, 198),
        'start': QColor(65, 252, 3),
        'end': QColor(252, 3, 3),
        'path': QColor(152, 111, 191)
    }
    
    borderColor = QColor(102, 102, 102)
    
    def __init__(self, x, y, size) -> None:
        super().__init__(0, 0, size, size)
        self.setPos(x * size, y * size)
        self.state = 'empty'
        self.updateColor()

    def updateColor(self) -> None:
        color = self.stateColorMap.get(self.state, self.stateColorMap['empty'])
        self.setBrush(QBrush(color))
        self.setPen(QPen(self.borderColor))
        
    def setState(self, state) -> None:
        self.state = state
        self.updateColor()
        
    def getState(self) -> str:
        return self.state