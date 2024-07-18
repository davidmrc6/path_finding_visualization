import time
import heapq

from src.solvers.BaseSearch import BaseSearch

class GBFSearch(BaseSearch):
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
            time.sleep(self.delay)

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
                            
        if not self._stop_event.is_set():
            self.noPathFound.emit()

    def startSearch(self):
        super().startSearch(self.gbfs)
