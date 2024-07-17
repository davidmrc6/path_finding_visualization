from PyQt5.QtWidgets import QMainWindow
from src.grid.GridWidget import GridWidget

class GridWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Path Finding Algorithm Visualization')
        
        self.gridWidget = GridWidget(rows=25, cols=40, cell_size=45)
        self.setCentralWidget(self.gridWidget)
