import os

from PyQt5.QtWidgets import QMainWindow, QPushButton, QDialog, QWidget
from PyQt5.QtCore import pyqtSlot

from src.grid.GridWidget import GridWidget

from src.solvers.BFSearch import BFSearch
from src.solvers.DFSearch import DFSearch
from src.solvers.DijkstraSearch import DijkstraSearch
from src.solvers.AStarSearch import AStarSearch
from src.solvers.GBFSearch import GBFSearch
from src.solvers.JumpPointSearch import JumpPointSearch
from src.solvers.BidirectionalSearch import BidirectionalSearch

from dialogs.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from dialogs.ResetDialog import ResetDialog

class GridWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle('Path Finding Algorithm Visualization')
        self.initUI()
        self.initAlgorithms()
        
    def initUI(self) -> None:
        # Initialize grid widget
        self.gridWidget = GridWidget(rows=25, cols=40, cell_size=45)
        self.setCentralWidget(self.gridWidget)
        
        # Initialize solve button
        solveButton = QPushButton('Solve', self)
        solveButton.setObjectName('solveButton')
        solveButton.clicked.connect(self.solverClicked)
        solveButton.setGeometry(10, 10, 100, 30)
        
        # Initialize reset button
        resetButton = QPushButton('Reset', self)
        resetButton.setObjectName('resetButton')
        resetButton.clicked.connect(self.resetClicked)
        resetButton.setGeometry(120, 10, 100, 30)
        
        self.applyStylesheet(solveButton, 'src/styles.qss')
        
    def initAlgorithms(self) -> None:
        
        algorithmToClassMap = {
            'bfs': BFSearch,
            'dfs': DFSearch,
            'dijkstra': DijkstraSearch,
            'astar': AStarSearch,
            'gbfs': GBFSearch,
            'jps': JumpPointSearch,
            'bisearch': BidirectionalSearch
        }
        
        self.algorithmToInstanceMap = {}
        for name, cls in algorithmToClassMap.items():
            instance = cls(self.gridWidget)
            instance.updateCellState.connect(self.gridWidget.setCellState)
            self.algorithmToInstanceMap[name] = instance
        
        self.currentSearch = None # keeps track of current algorithm
        
    def solverClicked(self) -> None:
        print("Solve button clicked")
        overlay = self.showBlurOverlay()
        dialog = AlgorithmSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selectedAlgorithm = dialog.getSelectedAlgorithm()
            
            self.currentSearch = self.algorithmToInstanceMap[selectedAlgorithm]
                
            if self.currentSearch:
                self.currentSearch.startSearch()
            
        overlay.deleteLater()
        
    def resetClicked(self) -> None:
        overlay = self.showBlurOverlay()
        dialog = ResetDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            option = dialog.getSelectedOption()
            self.gridWidget.resetGrid(option)
        overlay.deleteLater()
    
    def showBlurOverlay(self):
        overlay = QWidget(self)
        overlay.setObjectName("blurOverlay")
        overlay.setGeometry(self.rect())
        self.applyStylesheet(overlay, 'src/styles.qss')
        overlay.show()
        return overlay
        
    @pyqtSlot()
    def closeEvent(self, event):
        if self.currentSearch:
            self.currentSearch.stopSearch()
        event.accept()
        
    def applyStylesheet(self, widget, stylesheet_path) -> None:
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r') as file:
                widget.setStyleSheet(file.read())
