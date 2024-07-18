from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from functools import partial
import os

class AlgorithmSelectionDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Path Finding Algorithm")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(500, 350)

        self.algorithms = {
            'bfs': 'Breadth-First Search',
            'dfs': 'Depth-First Search',
            'dijkstra': 'Dijkstra`s Algorithm',
            'astar': 'A* algorithm',
            'gbfs': 'Greedy Best-First Search',
            'jps': 'Jump Point Search',
            'bisearch': 'Bidirectional Search'
        }
        
        algorithmInfoPath = os.path.join("res", "algorithmInfo.txt")
        
        self.algorithmInfo = self.loadAlgorithmInfo(algorithmInfoPath)

        layout = QVBoxLayout()

        title = QLabel("Select Path Finding Algorithm")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        icon_path = os.path.join("res", "info_icon.png")

        for key, name in self.algorithms.items():
            buttonLayout = QHBoxLayout()
            
            button = QPushButton(name)
            button.clicked.connect(partial(self.selectAlgorithm, key))
            buttonLayout.addWidget(button)
            
            infoButton = QPushButton()
            infoButton.setIcon(QIcon(icon_path))
            infoButton.setFixedSize(30, 30)
            infoButton.clicked.connect(partial(self.showAlgorithmInfo, key))
            buttonLayout.addWidget(infoButton)

            layout.addLayout(buttonLayout)

        self.setLayout(layout)
    
    def selectAlgorithm(self, key) -> None:
        self.selectedAlgorithm = key
        self.accept()
        
    def getSelectedAlgorithm(self) -> str:
        return self.selectedAlgorithm
    
    def loadAlgorithmInfo(self, filename: str):
        algorithms = {}
        with open(filename, 'r') as file:
            for line in file:
                key, name, info = line.strip().split(':')
                algorithms[key] = info
        return algorithms
    
    def showAlgorithmInfo(self, key: str) -> None:
        info = self.algorithmInfo.get(key, "No information available.")
        QMessageBox.information(self, "Algorithm Info", info)
