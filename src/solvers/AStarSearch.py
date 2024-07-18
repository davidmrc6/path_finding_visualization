import time
import heapq

from src.solvers.BaseSearch import BaseSearch

class AStarSearch(BaseSearch):
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self):
        start, end = self.findStartEnd()
        if not start or not end:
            return

        open_set = [(0, start)]
        g_costs = {start: 0}
        f_costs = {start: self.heuristic(start, end)}
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
                        tentative_g_cost = g_costs[current] + 1  # Assuming uniform cost
                        if (nr, nc) not in g_costs or tentative_g_cost < g_costs[(nr, nc)]:
                            g_costs[(nr, nc)] = tentative_g_cost
                            f_cost = tentative_g_cost + self.heuristic((nr, nc), end)
                            f_costs[(nr, nc)] = f_cost
                            heapq.heappush(open_set, (f_cost, (nr, nc)))
                            parent[(nr, nc)] = current
                            
        if not self._stop_event.is_set():
            self.noPathFound.emit()

    def startSearch(self):
        super().startSearch(self.astar)