"""
Module under which the GridWidget class is defined.

"""

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPainter

from src.grid.Cell import Cell

from src.eventHandlers.GridEventHandler import GridEventHandler

class GridWidget(QGraphicsView):
    """
    Class for defining a grid widget.
    
    This class represents a grid widget, which is a QGraphicsView object that contains a grid of cell objects.

    Args:
        QGraphicsView: The QGraphicsView class provides a widget for displaying the contents of a QGraphicsScene.
    """
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
    

    def initGrid(self) -> None:
        """
        Initializes the grid of cell objects.
        """
        for row in range(self.rows):
            cell_row = []
            for col in range(self.cols):
                cell = Cell(col, row, self.cell_size)
                self.scene.addItem(cell)
                cell_row.append(cell)
            self.cells.append(cell_row)
        
    @pyqtSlot(int, int, str)
    def setCellState(self, row, col, state) -> None:
        """
        Sets the state of a cell in the grid.

        Args:
            row: row of cell.
            col: col of cell.
            state: state of cell.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col].setState(state)
            
    def getStartNodeState(self) -> bool:
        """
        Returns the state of the start node:
            - True if start node exists.
            - False otherwise.
        """
        return self.hasStartNode
            
    def updateStartNodeState(self) -> None:
        """
        Updates the state of the start node.
        """
        self.hasStartNode = not self.hasStartNode
            
    def getEndNodeState(self) -> bool:
        """
        Returns the state of the end node:
            - True if end node exists.
            - False otherwise.
        """
        return self.hasEndNode
    
    def updateEndNodeState(self) -> None:
        """
        Updates the state of the end node.
        """
        self.hasEndNode = not self.hasEndNode 
        
    def resetGrid(self, option) -> None:
        """
        Resets the grid by calling a helper function based on the specified option.

        Args:
            option (str): option for resetting the grid.
        """
        if option == 'all':
            self.resetAll()
        elif option == 'checked_path':
            self.resetCheckedPath()
        elif option == 'obstacle':
            self.resetObstacles()
                    
    def resetAll(self) -> None:
        """
        Resets all cells in the grid.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                cell.setState('empty')
                self.hasStartNode = False
                self.hasEndNode = False
                
    def resetCheckedPath(self) -> None:
        """
        Resets all checked and path cells in the grid.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.getState() in ('checked', 'path'):
                    cell.setState('empty')
                    
    def resetObstacles(self) -> None:
        """
        Resets all obstacle cells in the grid.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.getState() == 'obstacle':
                    cell.setState('empty')
    
    def mousePressEvent(self, event) -> None:
        """
        Forwards mouse press event to event handler.
        """
        self.eventHandler.handleMousePress(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """
        Forwards mouse move event to event handler.
        """
        self.eventHandler.handleMouseMove(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """
        Forwards mouse release event to event handler.
        """
        self.eventHandler.handleMouseRelease(event)
        super().mouseReleaseEvent(event)