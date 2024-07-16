from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRectF, Qt

class Cell(QWidget):
        def __init__(self, x, y, size):
            super().__init__()
            self.x = x
            self.y = y
            self.size = size
            self.state = 'white'
            self.setFixedSize(size, size)

        def paintEvent(self, event):
            painter = QPainter(self)
            if self.state == 'white':
                color = QColor(255, 255, 255)
            # TODO add more colors later
            
            # TODO add exception handling when no color is set
            painter.setBrush(QBrush(color))
            painter.drawRect(0, 0, self.size, self.size)
            
        def setState(self, state):
            self.state = state
            self.update()