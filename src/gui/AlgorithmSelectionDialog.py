from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class AlgorithmSelectionDialog(QDialog):
    
    algorithms = {
        'bfs': 'Breadth-First Search',
        'dfs': 'Depth-First Search',
        'dijkstra': 'Dijkstra`s Algorithm',
        'astar': 'A* algorithm'
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Path Finding Algorithm")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        title = QLabel("Select Path Finding Algorithm")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        buttonLayout = QVBoxLayout()
        
        for key, name in self.algorithms.items():
            button = QPushButton(name)
            button.clicked.connect(lambda checked, k=key: self.selectAlgorithm(k))
            buttonLayout.addWidget(button)
        
        #bfsButton = QPushButton("Breadth-First Search")
        #bfsButton.clicked.connect(self.selectBfs)
        #buttonLayout.addWidget(bfsButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)
    
    def selectAlgorithm(self, key) -> None:
        self.selectedAlgorithm = key
        self.accept()
        
    def getSelectedAlgorithm(self) -> str:
        return self.selectedAlgorithm
