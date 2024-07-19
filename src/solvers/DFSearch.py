"""
Depth First Search algorithm implementation.
"""

import time

from src.solvers.BaseSearch import BaseSearch

class DFSearch(BaseSearch):
    """
    Depth First Search algorithm.
    
    The Depth First Search algorithm is a tree traversal algorithm. It starts
    at the root of the tree and explores all of the nodes at the present depth
    prior to moving onto the nodes at the next depth level.

    Args:
        BaseSearch: The base class for all search algorithms.
    """
    def dfs(self):
        """
        Implements the DFS algorithm to find the shortest path from
        the source node to the destination node.
        
        Algorithm:
            1. Initialize the stack with the source node.
            2. While the stack is not empty:
                2.1. Remove the last node from the stack.
                2.2. If the node has already been visited, continue to the
                next iteration.
                2.3. If the node is not the start or end node, update its
                state.
                2.4. If the node is the end node, trace the path and return.
                2.5. For each neighbor of the node:
                    2.5.1. If the neighbor is not the start or end node, push
                    it into the stack.
        """
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
        """
        Start the search algorithm.
        """
        super().startSearch(self.dfs)
