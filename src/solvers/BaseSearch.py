import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class BaseSearch(QObject):
    updateCellState = pyqtSignal(int, int, str)
    noPathFound = pyqtSignal()

    def __init__(self, gridWidget):
        super().__init__()
        self.gridWidget = gridWidget
        self.rows = gridWidget.rows
        self.cols = gridWidget.cols
        self.cells = gridWidget.cells
        self._stop_event = threading.Event()
        self.delay = 0.05

    def setDelay(self, speed):
        self.delay = 1 / speed

    def findStartEnd(self):
        start = end = None
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].getState() == 'start':
                    start = (row, col)
                elif self.cells[row][col].getState() == 'end':
                    end = (row, col)
        return start, end

    def tracePath(self, parent, end, start):
        current = end
        while current and not self._stop_event.is_set():
            row, col = current
            if current != end and current != start:
                self.updateCellState.emit(row, col, 'path')
            current = parent[current]
            time.sleep(0.1)

    def startSearch(self, algorithm):
        self._stop_event.clear()
        self.search_thread = threading.Thread(target=algorithm)
        self.search_thread.start()

    def stopSearch(self):
        self._stop_event.set()
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join()

    def isRunning(self):
        return self.search_thread and self.search_thread.is_alive()
