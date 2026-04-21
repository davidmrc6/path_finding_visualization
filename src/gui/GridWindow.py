"""
Module for defining the main window of the application.
    
"""
import os

from PyQt5.QtWidgets import QMainWindow, QPushButton, QDialog, QMessageBox, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot, Qt

from src.grid.GridWidget import GridWidget

from src.eventHandlers.WindowEventHandler import WindowEventHandler

from src.solvers.BFSearch import BFSearch
from src.solvers.DFSearch import DFSearch
from src.solvers.DijkstraSearch import DijkstraSearch
from src.solvers.AStarSearch import AStarSearch
from src.solvers.GBFSearch import GBFSearch
from src.solvers.BidirectionalSearch import BidirectionalSearch

from src.dialogs.AlgorithmSelectionDialog import AlgorithmSelectionDialog
from src.dialogs.ResetDialog import ResetDialog


class GridWindow(QMainWindow):
    """
    Main window of the application.
    
    This class represents the main window of the application, which
    involves creating a grid widget (of Cell objects) for visualizing
    path finding algorithms.

    Args:
        QMainWindow: The QMainWindow class provides a framework for building an application's user interface.
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        self.eventHandler = WindowEventHandler(self)
        
        self.setWindowTitle('Path Finding Algorithm Visualization')
        self.initUI()
        self.initAlgorithms()
        
    def initUI(self) -> None:
        """
        Initializes UI elements of main window.
        
        This method initializes:
            - Grid widget for visualizing path finding algorithms.
            - Solve button for starting the selected algorithm.
            - Reset button for resetting the grid.
            - Speed control slider for controlling the speed of the algorithm.
        """
        # Create a central widget and main layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(15, 15, 15, 15)
        mainLayout.setSpacing(10)

        # Initialize top bar layout for buttons and slider
        topBarLayout = QHBoxLayout()
        topBarLayout.setSpacing(10)
        
        # Initialize solve button
        solveButton = QPushButton('Solve', self)
        solveButton.setObjectName('solveButton')
        solveButton.clicked.connect(self.eventHandler.solverClicked)
        topBarLayout.addWidget(solveButton)
        
        # Initialize reset button
        resetButton = QPushButton('Reset', self)
        resetButton.setObjectName('resetButton')
        resetButton.clicked.connect(self.eventHandler.resetClicked)
        topBarLayout.addWidget(resetButton)
        
        # Add a stretch to separate buttons from slider
        topBarLayout.addStretch()

        # Speed label
        speedLabel = QLabel('Speed:')
        topBarLayout.addWidget(speedLabel)

        # Initialize speed control slider
        self.speedSlider = QSlider(Qt.Horizontal, self)
        self.speedSlider.setObjectName('speedSlider')
        self.speedSlider.setRange(1, 100)  # Speed range from 1 to 100
        self.speedSlider.setValue(50)  # Default value
        self.speedSlider.setFixedWidth(150)
        self.speedSlider.valueChanged.connect(self.eventHandler.changeSpeed)
        topBarLayout.addWidget(self.speedSlider)

        mainLayout.addLayout(topBarLayout)

        # Initialize grid widget
        self.gridWidget = GridWidget(rows=30, cols=40, cell_size=45)
        mainLayout.addWidget(self.gridWidget)
        
    def initAlgorithms(self) -> None:
        """
        Initializes path finding algorithms.
        
        This methods creates instances of path finder objects.
        """
        algorithmToClassMap = {
            'bfs': BFSearch,
            'dfs': DFSearch,
            'dijkstra': DijkstraSearch,
            'astar': AStarSearch,
            'gbfs': GBFSearch,
            'bisearch': BidirectionalSearch
        }
        
        self.algorithmToInstanceMap = {}
        for name, cls in algorithmToClassMap.items():
            instance = cls(self.gridWidget)
            instance.updateCellState.connect(self.gridWidget.setCellState)
            instance.noPathFound.connect(self.eventHandler.noPathFoundHandler)
            self.algorithmToInstanceMap[name] = instance
        
        self.currentSearch = None # keeps track of current algorithm
        
    @pyqtSlot()
    def closeEvent(self, event) -> None:
        """
        Handle the close event for the window.
        
        This method is called when the window recieves a close event. It stops 
        the thread on which the current search algorithm is running and accepts the
        event to close the window.

        Args:
            event: The close event to be handled.
        """
        self.stopCurrentSearch()
        event.accept()
        
    def stopCurrentSearch(self) -> None:
        """
        Stops the current search algorithm if it is running.
        """
        if self.currentSearch and self.currentSearch.isRunning():
            self.currentSearch.stopSearch()
        self.currentSearch = None
