import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class BidirectionalSearch(QObject):
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

    def bidirectionalSearch(self):
        start, end = self.findStartEnd()
        if not start or not end:
            return

        queue_start = [start]
        queue_end = [end]
        visited_start = {start}
        visited_end = {end}
        parent_start = {start: None}
        parent_end = {end: None}

        def trace_path(meeting_point):
            path_start = []
            path_end = []
            current = meeting_point
            while current:
                path_start.append(current)
                current = parent_start[current]
            current = meeting_point
            while current:
                path_end.append(current)
                current = parent_end[current]
            full_path = path_start[::-1] + path_end[1:]
            for node in full_path:
                row, col = node
                if node != start and node != end:
                    self.updateCellState.emit(row, col, 'path')
                time.sleep(0.05)

        while queue_start and queue_end and not self._stop_event.is_set():
            if queue_start:
                current_start = queue_start.pop(0)
                row_start, col_start = current_start

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row_start + dr, col_start + dc
                    neighbor_start = (nr, nc)
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and neighbor_start not in visited_start:
                        if self.cells[nr][nc].getState() != 'obstacle':
                            parent_start[neighbor_start] = current_start
                            visited_start.add(neighbor_start)
                            queue_start.append(neighbor_start)
                            if neighbor_start in visited_end:
                                trace_path(neighbor_start)
                                return
                            if neighbor_start != start and neighbor_start != end:
                                self.updateCellState.emit(nr, nc, 'checked')
                            time.sleep(0.05)

            if queue_end:
                current_end = queue_end.pop(0)
                row_end, col_end = current_end

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row_end + dr, col_end + dc
                    neighbor_end = (nr, nc)
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and neighbor_end not in visited_end:
                        if self.cells[nr][nc].getState() != 'obstacle':
                            parent_end[neighbor_end] = current_end
                            visited_end.add(neighbor_end)
                            queue_end.append(neighbor_end)
                            if neighbor_end in visited_start:
                                trace_path(neighbor_end)
                                return
                            if neighbor_end != start and neighbor_end != end:
                                self.updateCellState.emit(nr, nc, 'checked')
                            time.sleep(0.05)

    def startSearch(self):
        self._stop_event.clear()
        self.search_thread = threading.Thread(target=self.bidirectionalSearch)
        self.search_thread.start()

    def stopSearch(self):
        self._stop_event.set()
        if self.search_thread.is_alive():
            self.search_thread.join()
