from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class AlgorithmSelectionDialog(QDialog):
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

        bfsButton = QPushButton("Breadth-First Search")
        bfsButton.clicked.connect(self.selectBfs)
        buttonLayout.addWidget(bfsButton)

        # Add more algorithm buttons here
        # dfs_button = QPushButton("Depth-First Search")
        # dfs_button.clicked.connect(self.select_dfs)
        # button_layout.addWidget(dfs_button)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def selectBfs(self):
        self.selectedAlgorithm = 'bfs'
        self.accept()

    # def selectDfs(self):
    #     self.selectedAlgorithm = 'dfs'
    #     self.accept()
