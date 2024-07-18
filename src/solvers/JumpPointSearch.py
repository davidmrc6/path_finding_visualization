import time
import heapq

from src.solvers.BaseSearch import BaseSearch

class JumpPointSearch(BaseSearch):
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
            
    def startSearch(self):
        super().startSearch(self.jps)