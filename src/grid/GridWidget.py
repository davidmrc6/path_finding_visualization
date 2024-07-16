from PyQt5.QtWidgets import QWidget, QGridLayout
from src.grid.Cell import Cell

class GridWidget(QWidget):
    def __init__(self, rows, cols, cell_size):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.cells = []
        for row in range(rows):
            cell_row = []
            for col in range(cols):
                cell = Cell(row, col, cell_size)
                self.layout.addWidget(cell, row, col)
                cell_row.append(cell)
            self.cells.append(cell_row)

        self.setLayout(self.layout)
        
    def setCellState(self, row, col, state):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col].set_state(state)