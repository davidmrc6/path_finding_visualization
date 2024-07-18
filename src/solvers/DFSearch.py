import time

from src.solvers.BaseSearch import BaseSearch

class DFSearch(BaseSearch):
    def dfs(self):
        start, end = self.findStartEnd()
        if not start or not end:
            return
        
        stack = [start]
        visited = set()
        parent = {start: None}

        while stack and not self._stop_event.is_set():
            current = stack.pop()
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
                    if self.cells[nr][nc].getState() in ('empty', 'end') and (nr, nc) not in visited:
                        stack.append((nr, nc))
                        parent[(nr, nc)] = current
                        
        if not self._stop_event.is_set():
            self.noPathFound.emit()
            
    def startSearch(self):
        super().startSearch(self.dfs)
