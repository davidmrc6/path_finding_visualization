from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from src.grid.Cell import Cell

from src.eventHandlers.GridEventHandler import GridEventHandler

class GridWidget(QGraphicsView):
    def __init__(self, rows, cols, cell_size) -> None:
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cells = []
        self.initGrid()

        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.eventHandler = GridEventHandler(self)
        
        self.hasStartNode = False
        self.hasEndNode = False
    
    '''
    Initializes grid of cell objects
    '''
    def initGrid(self) -> None:
        for row in range(self.rows):
            cell_row = []
            for col in range(self.cols):
                cell = Cell(col, row, self.cell_size)
                self.scene.addItem(cell)
                cell_row.append(cell)
            self.cells.append(cell_row)
        
    def setCellState(self, row, col, state) -> None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col].setState(state)
            
    def getStartNodeState(self) -> bool:
        return self.hasStartNode
            
    def updateStartNodeState(self) -> None:
        self.hasStartNode = not self.hasStartNode
            
    def getEndNodeState(self) -> bool:
        return self.hasEndNode
    
    def updateEndNodeState(self) -> None:
        self.hasEndNode = not self.hasEndNode 
    
    '''
    Forwards mouse events to eventHandler
    ''' 
    def mousePressEvent(self, event) -> None:
        self.eventHandler.handleMousePress(event)
        super().mousePressEvent(event)