from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRectF, Qt

class Cell(QGraphicsRectItem):
        def __init__(self, x, y, size):
            super().__init__(0, 0, size, size)
            self.setPos(x * size, y * size)
            self.state = 'white'
            self.updateColor()

        def updateColor(self):
            if self.state == 'white':
                color = QColor(255, 255, 255)
            # TODO add more colors later
            
            # TODO add exception handling when no color is set
            self.setBrush(QBrush(color))
            
        def setState(self, state):
            self.state = state
            self.update()