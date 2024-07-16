from PyQt5.QtWidgets import QMainWindow
from src.grid.GridWidget import GridWidget

class GridWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Path Finding Algorithm Visualization')
        
        self.gridWidget = GridWidget(rows=20, cols=20, cell_size=50)
        self.setCentralWidget(self.gridWidget)
