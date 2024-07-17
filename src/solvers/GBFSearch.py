import time
import threading
import heapq
from PyQt5.QtCore import pyqtSignal, QObject

class GBFSearch(QObject):
    updateCellState = pyqtSignal(int, int, str)

    def __init__(self, gridWidget):
        super().__init__()
        self.gridWidget = gridWidget
        self.rows = gridWidget.rows
        self.cols = gridWidget.cols
        self.cells = gridWidget.cells
        self._stop_event = threading.Event()

    def findStartEnd(self):
        start = end = None
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].getState() == 'start':
                    start = (row, col)
                elif self.cells[row][col].getState() == 'end':
                    end = (row, col)
        return start, end

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def gbfs(self):
        start, end = self.findStartEnd()
        if not start or not end:
            return

        open_set = [(0, start)]
        parent = {start: None}
        visited = set()

        while open_set and not self._stop_event.is_set():
            current_f, current = heapq.heappop(open_set)
            row, col = current

            if current in visited:
                continue

            visited.add(current)
            if current != start and current != end:
                self.updateCellState.emit(row, col, 'checked')
            time.sleep(0.05)

            if current == end:
                self.tracePath(parent, end, start)
                return

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.cells[nr][nc].getState() in ('empty', 'end'):
                        if (nr, nc) not in visited:
                            heapq.heappush(open_set, (self.heuristic((nr, nc), end), (nr, nc)))
                            parent[(nr, nc)] = current

    def tracePath(self, parent, end, start):
        current = end
        while current and not self._stop_event.is_set():
            row, col = current
            if current != end and current != start:
                self.updateCellState.emit(row, col, 'path')
            current = parent[current]
            time.sleep(0.1)

    def startSearch(self):
        self._stop_event.clear()
        self.search_thread = threading.Thread(target=self.gbfs)
        self.search_thread.start()

    def stopSearch(self):
        self._stop_event.set()
        if self.search_thread.is_alive():
            self.search_thread.join()
