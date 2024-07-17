from PyQt5.QtCore import Qt
from src.grid.Cell import Cell

class GridEventHandler:
    def __init__(self, gridWidget) -> None:
        self.gridWidget = gridWidget
        
    def handleMousePress(self, event) -> None:
        scenePos = self.gridWidget.mapToScene(event.pos())
        item = self.gridWidget.scene.itemAt(scenePos, self.gridWidget.transform())
        
        if isinstance(item, Cell):
            if event.button() == Qt.LeftButton:
                item.setState('obstacle')
            elif event.button() == Qt.RightButton:
                item.setState('empty')