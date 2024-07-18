import time
import threading
import heapq
from PyQt5.QtCore import pyqtSignal, QObject

class JumpPointSearch(QObject):
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

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def jump(self, current, direction, end):
        x, y = current
        dx, dy = direction
        next_pos = (x + dx, y + dy)

        if not (0 <= next_pos[0] < self.rows and 0 <= next_pos[1] < self.cols) or self.cells[next_pos[0]][next_pos[1]].getState() == 'obstacle':
            return None

        if next_pos == end:
            return next_pos

        if dx != 0 and dy != 0:
            if (0 <= next_pos[0] + dx < self.rows and 0 <= next_pos[1] < self.cols and 
                self.cells[next_pos[0] + dx][next_pos[1]].getState() != 'obstacle'):
                return next_pos
            if (0 <= next_pos[0] < self.rows and 0 <= next_pos[1] + dy < self.cols and 
                self.cells[next_pos[0]][next_pos[1] + dy].getState() != 'obstacle'):
                return next_pos
            if self.jump(next_pos, (dx, 0), end) or self.jump(next_pos, (0, dy), end):
                return next_pos
        elif dx != 0:
            if (0 <= next_pos[0] + dx < self.rows and 0 <= next_pos[1] < self.cols and 
                self.cells[next_pos[0] + dx][next_pos[1]].getState() != 'obstacle'):
                return next_pos
        elif dy != 0:
            if (0 <= next_pos[0] < self.rows and 0 <= next_pos[1] + dy < self.cols and 
                self.cells[next_pos[0]][next_pos[1] + dy].getState() != 'obstacle'):
                return next_pos

        return self.jump(next_pos, direction, end)

    def identifySuccessors(self, current, end):
        successors = []
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            jump_point = self.jump(current, direction, end)
            if jump_point:
                successors.append(jump_point)
        return successors

    def jps(self):
        start, end = self.findStartEnd()
        if not start or not end:
            return

        open_set = [(0, start)]
        g_costs = {start: 0}
        parent = {start: None}
        visited = set()

        while open_set and not self._stop_event.is_set():
            _, current = heapq.heappop(open_set)
            row, col = current

            if current in visited:
                continue

            visited.add(current)
            if current != start and current != end:
                self.updateCellState.emit(row, col, 'checked')
            time.sleep(self.delay)

            if current == end:
                self.tracePath(parent, end, start)
                return

            for neighbor in self.identifySuccessors(current, end):
                if neighbor not in visited:
                    tentative_g_cost = g_costs[current] + 1  # Assuming uniform cost
                    if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                        g_costs[neighbor] = tentative_g_cost
                        f_cost = tentative_g_cost + self.heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_cost, neighbor))
                        parent[neighbor] = current
                        
        if not self._stop_event.is_set():
            self.noPathFound.emit()

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
        self.search_thread = threading.Thread(target=self.jps)
        self.search_thread.start()

    def stopSearch(self):
        self._stop_event.set()
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join()

    def isRunning(self):
        return self.search_thread and self.search_thread.is_alive()