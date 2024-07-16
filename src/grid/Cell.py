from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor


class Cell(QRectF):
        def __init__(self, x, y, size):
            super().__init__(x, y, size, size)
            self.state = None

        def draw(self, painter):
            if self.state == 'start':
                painter.setBrush(QColor(0, 255, 0))  # Green
            elif self.state == 'end':
                painter.setBrush(QColor(255, 0, 0))  # Red
            elif self.state == 'obstacle':
                painter.setBrush(QColor(0, 0, 0))  # Black
            else:
                painter.setBrush(QColor(255, 255, 255))  # White

            painter.drawRect(self)