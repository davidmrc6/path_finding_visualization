"""
Module for defining the main window of the application.
    
"""

import os

from PyQt5.QtWidgets import QMainWindow, QPushButton, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot

from src.grid.GridWidget import GridWidget

from src.eventHandlers.WindowEventHandler import WindowEventHandler

from src.solvers.BFSearch import BFSearch
from src.solvers.DFSearch import DFSearch
from src.solvers.DijkstraSearch import DijkstraSearch
from src.solvers.AStarSearch import AStarSearch
from src.solvers.GBFSearch import GBFSearch
from src.solvers.JumpPointSearch import JumpPointSearch
from src.solvers.BidirectionalSearch import BidirectionalSearch

from src.dialogs.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from src.dialogs.ResetDialog import ResetDialog


class GridWindow(QMainWindow):
    """
    Main window of the application.
    
    This class represents the main window of the application, which
    involves creating a grid widget (of Cell objects) for visualizing
    path finding algorithms.
    
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        self.eventHandler = WindowEventHandler(self)
        
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
        solveButton.clicked.connect(self.eventHandler.solverClicked)
        solveButton.setGeometry(10, 10, 100, 30)
        
        # Initialize reset button
        resetButton = QPushButton('Reset', self)
        resetButton.setObjectName('resetButton')
        resetButton.clicked.connect(self.eventHandler.resetClicked)
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
            instance.noPathFound.connect(self.noPathFoundHandler)
            self.algorithmToInstanceMap[name] = instance
        
        self.currentSearch = None # keeps track of current algorithm
        
    @pyqtSlot()
    def closeEvent(self, event):
        if self.currentSearch and self.currentSearch.search_thread.is_alive():
            self.currentSearch.stopSearch()
        event.accept()
        
    def applyStylesheet(self, widget, stylesheet_path) -> None:
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r') as file:
                widget.setStyleSheet(file.read())


    def noPathFoundHandler(self):
        QMessageBox.warning(self, "No Path Found", "There is no possible path from start to end.")