from PyQt5.QtCore import Qt, QPointF, QPropertyAnimation, QByteArray
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsScene
from PyQt5.QtGui import QFont
from src.grid.Cell import Cell
from src.custom.CustomGraphicsTextItem import CustomGraphicsTextItem

class GridEventHandler:
    def __init__(self, gridWidget) -> None:
        self.gridWidget = gridWidget
        self.activePopups = {}
        
    def handleMousePress(self, event) -> None:
        scenePos = self.gridWidget.mapToScene(event.pos())
        item = self.gridWidget.scene.itemAt(scenePos, self.gridWidget.transform())
        
        if isinstance(item, Cell):
            
            # Left button is used for setting start and end nodes
            if event.button() == Qt.LeftButton:
                pass
            
            # Right button is used for setting (and removing) obstacles
            if event.button() == Qt.RightButton:
                if item.getState() == 'empty':
                    item.setState('obstacle')
                    self.showPopupText(item, 'Obstacle')
                elif item.getState() == 'obstacle':
                    item.setState('empty')
                    self.showPopupText(item, 'Empty')
                
    def showPopupText(self, cell: Cell, text: str) -> None:
        cellPos = (cell.x(), cell.y())

        # Remove existing popup if present
        if cellPos in self.activePopups:
            popupText, animation = self.activePopups[cellPos]
            animation.stop()
            self.gridWidget.scene.removeItem(popupText)

        popupText = CustomGraphicsTextItem(text)
        popupText.setDefaultTextColor(Qt.black)
        popupText.setPos(cell.x(), cell.y() - cell.rect().height() / 2)
        self.gridWidget.scene.addItem(popupText)
        
        # Set font
        font = QFont("Segoe UI", 8)
        popupText.setFont(font)

        # Animation to fade out the text
        animation = QPropertyAnimation(popupText, b"opacity")
        animation.setDuration(1000)  # 1 second
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.finished.connect(lambda: self.removePopupText(cellPos))
        animation.start()

        self.activePopups[cellPos] = (popupText, animation)

    def removePopupText(self, cellPos) -> None:
        popupText, _ = self.activePopups.pop(cellPos, (None, None))
        if popupText:
            self.gridWidget.scene.removeItem(popupText)