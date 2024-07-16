from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView

class GridWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Placeholder')
        self.setGeometry(100, 100, 800, 800)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        