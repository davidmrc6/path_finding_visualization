import heapq
import time

from src.solvers.BaseSearch import BaseSearch

class DijkstraSearch(BaseSearch):
    def dijkstra(self):
        start, end = self.findStartEnd()
        if not start or not end:
            return

        priority_queue = [(0, start)]
        distances = {start: 0}
        parent = {start: None}
        visited = set()

        while priority_queue and not self._stop_event.is_set():
            current_distance, current = heapq.heappop(priority_queue)
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
                        new_distance = current_distance + 1  # Assuming uniform cost
                        if (nr, nc) not in distances or new_distance < distances[(nr, nc)]:
                            distances[(nr, nc)] = new_distance
                            heapq.heappush(priority_queue, (new_distance, (nr, nc)))
                            parent[(nr, nc)] = current
                            
        if not self._stop_event.is_set():
            self.noPathFound.emit()
            
    def startSearch(self):
        super().startSearch(self.dijkstra)
