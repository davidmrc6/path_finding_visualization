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
        # TODO instantiate search type after selection?
        self.bfs = BFSearch(self.gridWidget)
        self.bfs.updateCellState.connect(self.gridWidget.setCellState)
        
        self.dfs = DFSearch(self.gridWidget)
        self.dfs.updateCellState.connect(self.gridWidget.setCellState)
        
        self.dijkstra = DijkstraSearch(self.gridWidget)
        self.dijkstra.updateCellState.connect(self.gridWidget.setCellState)
        
        self.astar = AStarSearch(self.gridWidget)
        self.astar.updateCellState.connect(self.gridWidget.setCellState)
        
        self.gbfs = GBFSearch(self.gridWidget)
        self.gbfs.updateCellState.connect(self.gridWidget.setCellState)
        
        self.jps = JumpPointSearch(self.gridWidget)
        self.jps.updateCellState.connect(self.gridWidget.setCellState)
        
        self.bisearch = BidirectionalSearch(self.gridWidget)
        self.bisearch.updateCellState.connect(self.gridWidget.setCellState)
        
        self.algorithmToInstanceMap = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'dijkstra': self.dijkstra,
            'astar': self.astar,
            'gbfs': self.gbfs,
            'jps': self.jps,
            'bisearch': self.bisearch
        }
        
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
