"""
This module contains the GridEventHandler class, which is responsible for handling mouse events on the grid.

"""

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QFont
from src.grid.Cell import Cell
from src.custom.CustomGraphicsTextItem import CustomGraphicsTextItem

class GridEventHandler:
    """
    Class that handles mouse events on the grid.
    """
    def __init__(self, gridWidget) -> None:
        self.gridWidget = gridWidget
        self.activePopups = {}
        self.dragging = False
        self.dragState = None
        
    def handleMousePress(self, event) -> None:
        """
        Handle mouse press events on the grid.
        
        This method checks whether the user has left-clicked or right-clicked over
        a cell in the grid and calls the corresponding handler method.

        Args:
            event: the mouse press event.
        """
        item = self.getCellFromEvent(event)
        
        if isinstance(item, Cell):
            if event.button() == Qt.LeftButton:
                self.handleLeftClick(item)
            elif event.button() == Qt.RightButton:
                self.dragging = True
                self.setDragState(item)
                self.handleRightClick(item)
                    
    def handleMouseRelease(self, event) -> None:
        """
        Handle mouse release events on the grid.
        
        When the user releases the right mouse button, this method sets the dragging
        flag to False and resets the drag state.

        Args:
            event: the mouse release event.
        """
        if event.button() == Qt.RightButton:
            self.dragging = False
            self.dragState = None
    
    def handleMouseMove(self, event) -> None:
        """
        Handle mouse move events on the grid.
        
        This method checks whether the user is dragging the mouse over the grid.
        If the user is dragging the mouse, it calls the handleRightClick method and
        passes the cell that the mouse is currently over.

        Args:
            event: the mouse move event.
        """
        if self.dragging:
            item = self.getCellFromEvent(event)
            if isinstance(item, Cell):
                self.handleRightClick(item)
    
    def handleLeftClick(self, item: Cell) -> None:
        """
        Handle left-click events on the grid.
        
        This method is used to set the start and end nodes on the grid.

        Args:
            item (Cell): the cell that the user has clicked on.
        """
        if item.getState() == 'empty':
            if not self.gridWidget.getStartNodeState():
                self.updateCellState(item, 'start', 'Start')
                self.gridWidget.updateStartNodeState()
            elif not self.gridWidget.getEndNodeState():
                self.updateCellState(item, 'end', 'End')
                self.gridWidget.updateEndNodeState()
        elif item.getState() == 'start':
            self.updateCellState(item, 'empty', 'Empty')
            self.gridWidget.updateStartNodeState()
        elif item.getState() == 'end':
            self.updateCellState(item, 'empty', 'Empty')
            self.gridWidget.updateEndNodeState()
            
    def handleRightClick(self, item: Cell) -> None:
        """
        Handle right-click events on the grid.
        
        This method is used to set obstacles on the grid. It also supports
        dragging the mouse to set multiple obstacles at once.

        Args:
            item (Cell): the cell that the user has right-clicked on.
        """
        if self.dragState == 'obstacle' and item.getState() == 'empty':
            self.updateCellState(item, 'obstacle', 'Obstacle')
        elif self.dragState == 'empty' and item.getState() == 'obstacle':
            self.updateCellState(item, 'empty', 'Empty')
    
    def updateCellState(self, item: Cell, newState: str, popupText: str) -> None:
        """
        Update the state of a cell on the grid.
        """
        item.setState(newState)
        self.showPopupText(item, popupText)
        
    def getCellFromEvent(self, event) -> Cell:
        """
        Get the cell that the user has clicked on.

        Args:
            event: the mouse event.

        Returns:
            Cell: returns the cell that the user has clicked on.
        """
        scenePos = self.gridWidget.mapToScene(event.pos())
        return self.gridWidget.scene.itemAt(scenePos, self.gridWidget.transform())
    
    def setDragState(self, item: Cell) -> None:
        """
        Set the drag state of the grid.
        
        Once the user has right-clicked and started dragging over the grid, this
        method ensures that all cells that the user drags over will be set to either
        'obstacle' or 'empty'. This is so that the user doesn't accidentally set
        a cell to 'obstacle' and back to 'empty' on the same drag.

        Args:
            item (Cell): _description_
        """
        if item.getState() == 'empty':
            self.dragState = 'obstacle'
        elif item.getState() == 'obstacle':
            self.dragState = 'empty'
    
    def showPopupText(self, cell: Cell, text: str) -> None:
        """
        Show a popup text above a cell on the grid.
        
        This method is used to show a popup text above a cell on the grid once the user clicks
        on it. The popup text will display the state of the cell (e.g. 'Start', 'End', 'Obstacle').
        This is to avoid confusion when the user is setting the start and end nodes or obstacles.

        Args:
            cell (Cell): the cell over which the text will pop up.
            text (str): the text which will be displayed in the popup - represents the state of the cell.
        """
        # Get position of cell
        cellPos = (cell.x(), cell.y())

        # Check if cell is already active
        if cellPos in self.activePopups:
            popupText, animation = self.activePopups[cellPos]
            animation.stop()
            self.gridWidget.scene.removeItem(popupText)

        # Call custom graphics text item
        popupText = CustomGraphicsTextItem(text)
        popupText.setDefaultTextColor(Qt.black)
        popupText.setPos(cell.x(), cell.y() - cell.rect().height() / 2)
        self.gridWidget.scene.addItem(popupText)

        font = QFont("Segoe UI", 8)
        popupText.setFont(font)

        animation = QPropertyAnimation(popupText, b"opacity")
        animation.setDuration(1000)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.finished.connect(lambda: self.removePopupText(cellPos))
        animation.start()

        self.activePopups[cellPos] = (popupText, animation)

    def removePopupText(self, cellPos) -> None:
        """
        Remove the popup text from the grid.

        Args:
            cellPos: the position of the cell.
        """
        popupText, _ = self.activePopups.pop(cellPos, (None, None))
        if popupText:
            self.gridWidget.scene.removeItem(popupText)
