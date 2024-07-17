from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import pyqtSlot
from src.grid.GridWidget import GridWidget
from src.solvers.BFSearch import BFSearch
from src.solvers.DFSearch import DFSearch
from src.gui.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from PyQt5.QtWidgets import QDialog, QWidget
import os

class GridWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle('Path Finding Algorithm Visualization')
        self.initUI()
        
        # TODO instantiate search type after selection?
        self.bfs = BFSearch(self.gridWidget)
        self.bfs.updateCellState.connect(self.gridWidget.setCellState)
        
        self.dfs = DFSearch(self.gridWidget)
        self.dfs.updateCellState.connect(self.gridWidget.setCellState)
        
        self.currentSearch = None # keeps track of current algorithm
        
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
        overlay = self.showBlurOverlay()
        dialog = AlgorithmSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selectedAlgorithm = dialog.getSelectedAlgorithm()
            
            # TODO fix code repetition
            if selectedAlgorithm == 'bfs':
                self.currentSearch = self.bfs
                
            elif selectedAlgorithm == 'dfs':
                self.currentSearch = self.dfs
                
            elif selectedAlgorithm == 'dijkstra':
                self.currentSearch = self.dijkstra
                
            elif selectedAlgorithm == 'astar':
                self.currentSearch = self.astar
                
            if self.currentSearch:
                self.currentSearch.startSearch()
            
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
