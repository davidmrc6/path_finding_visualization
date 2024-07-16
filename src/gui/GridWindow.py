from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter
import sys
import os

# Add the parent directory to the p‚ath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.grid.Cell import Cell

class GridWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.cells = []
        
        self.setWindowTitle('Placeholder')
        self.setGeometry(100, 100, 800, 800)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        
        self.initGrid()
        
    def initGrid(self):
        grid_size = 10
        cell_size = 50
        margin = 10
        
        for i in range(grid_size):
            for j in range(grid_size):
                x = margin + j * (cell_size + margin)
                y = margin + i * (cell_size + margin)
                cell = Cell(x, y, cell_size)
                self.scene.addItem(cell)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        for cell in self.cells:
            cell.draw(self.scene)
