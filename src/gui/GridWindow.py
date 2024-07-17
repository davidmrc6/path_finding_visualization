from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import pyqtSlot
from src.grid.GridWidget import GridWidget
from src.solvers.BFSearch import BFSearch
import os

class GridWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle('Path Finding Algorithm Visualization')
        self.initUI()
        
        self.bfs = BFSearch(self.gridWidget)
        self.bfs.updateCellState.connect(self.gridWidget.setCellState)
        
    def initUI(self) -> None:
        # Initialize grid widget
        self.gridWidget = GridWidget(rows=25, cols=40, cell_size=45)
        self.setCentralWidget(self.gridWidget)
        
        # Initialize solve button
        solveButton = QPushButton('Solve', self)
        solveButton.setObjectName('solveButton')
        solveButton.clicked.connect(self.solverClicked)
        solveButton.setGeometry(10, 10, 100, 30)
        
        self.applyStylesheet(solveButton, 'src/styles.qss')
        
    def solverClicked(self) -> None:
        print("Solve button clicked")
        self.bfs.start_search()
        
    @pyqtSlot()
    def closeEvent(self, event):
        self.bfs.stop_search()
        event.accept()
        
    def applyStylesheet(self, widget, stylesheet_path) -> None:
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r') as file:
                widget.setStyleSheet(file.read())
