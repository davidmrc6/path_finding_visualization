from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from src.grid.Cell import Cell

class GridWidget(QGraphicsView):
    def __init__(self, rows, cols, cell_size):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cells = []
        self.initGrid()

        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scale(1, 1)  # Initial scale factor
        
    def initGrid(self):
        for row in range(self.rows):
            cell_row = []
            for col in range(self.cols):
                cell = Cell(col, row, self.cell_size)
                self.scene.addItem(cell)
                cell_row.append(cell)
            self.cells.append(cell_row)
        
    def setCellState(self, row, col, state):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col].set_state(state)