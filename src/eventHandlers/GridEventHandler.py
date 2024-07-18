from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QFont
from src.grid.Cell import Cell
from src.custom.CustomGraphicsTextItem import CustomGraphicsTextItem

class GridEventHandler:
    def __init__(self, gridWidget) -> None:
        self.gridWidget = gridWidget
        self.activePopups = {}
        self.dragging = False
        self.dragState = None
        
    def handleMousePress(self, event) -> None:
        item = self.getCellFromEvent(event)
        
        if isinstance(item, Cell):
            if event.button() == Qt.LeftButton:
                self.handleLeftClick(item)
            elif event.button() == Qt.RightButton:
                self.dragging = True
                self.setDragState(item)
                self.handleRightClick(item)
                    
    def handleMouseRelease(self, event) -> None:
        if event.button() == Qt.RightButton:
            self.dragging = False
            self.dragState = None
    
    def handleMouseMove(self, event) -> None:
        if self.dragging:
            item = self.getCellFromEvent(event)
            if isinstance(item, Cell):
                self.handleRightClick(item)
    
    def handleLeftClick(self, item: Cell) -> None:
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
        if self.dragState == 'obstacle' and item.getState() == 'empty':
            self.updateCellState(item, 'obstacle', 'Obstacle')
        elif self.dragState == 'empty' and item.getState() == 'obstacle':
            self.updateCellState(item, 'empty', 'Empty')
    
    def updateCellState(self, item: Cell, newState: str, popupText: str) -> None:
        item.setState(newState)
        self.showPopupText(item, popupText)
        
    def getCellFromEvent(self, event):
        scenePos = self.gridWidget.mapToScene(event.pos())
        return self.gridWidget.scene.itemAt(scenePos, self.gridWidget.transform())
    
    def setDragState(self, item: Cell) -> None:
        if item.getState() == 'empty':
            self.dragState = 'obstacle'
        elif item.getState() == 'obstacle':
            self.dragState = 'empty'
    
    def showPopupText(self, cell: Cell, text: str) -> None:
        cellPos = (cell.x(), cell.y())

        if cellPos in self.activePopups:
            popupText, animation = self.activePopups[cellPos]
            animation.stop()
            self.gridWidget.scene.removeItem(popupText)

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
        popupText, _ = self.activePopups.pop(cellPos, (None, None))
        if popupText:
            self.gridWidget.scene.removeItem(popupText)
