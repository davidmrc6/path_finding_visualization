"""
Module under which the Cell class is defined.
"""

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QColor, QBrush, QPen

class Cell(QGraphicsRectItem):
    """
    Class for defining a cell object in the grid.
    
    This class represents a cell object in the grid, which can be in one of the following states:
        - empty: cell is empty;
        - obstacle: cell is an obstacle, i.e., not traversable;
        - checked: cell has been checked by a path finder;
        - start: cell marks the source node for the path finder;
        - end: cell marks the destination node for the path finder;
        - path: cell is part of the path found by the path finder.

    Args:
        QGraphicsRectItem: The QGraphicsRectItem class provides a rectangle item that you can add to a QGraphicsScene.
    """
    
    # Dictionary mapping state of cell to color in grid
    stateColorMap = {
        'empty': QColor(245, 245, 245),
        'obstacle': QColor(102, 102, 102),
        'checked': QColor(198, 198, 198),
        'start': QColor(65, 252, 3),
        'end': QColor(252, 3, 3),
        'path': QColor(152, 111, 191)
    }
    
    # Color of border of cell
    borderColor = QColor(102, 102, 102)
    
    def __init__(self, x, y, size) -> None:
        super().__init__(0, 0, size, size)
        self.setPos(x * size, y * size)
        self.state = 'empty'
        self.updateColor()

    def updateColor(self) -> None:
        """
        Updates the color of the cell based on its state.
        """
        color = self.stateColorMap.get(self.state, self.stateColorMap['empty'])
        self.setBrush(QBrush(color))
        self.setPen(QPen(self.borderColor))
        
    def setState(self, state) -> None:
        """
        Sets the state of the cell.

        Args:
            state (str): state of cell.
        """
        self.state = state
        self.updateColor()
        
    def getState(self) -> str:
        """
        Returns the state of the cell.

        Returns:
            str: state of cell.
        """
        return self.state