"""
This module contains the implementation of the BFS search algorithm.
"""

import time

from src.solvers.BaseSearch import BaseSearch

class BFSearch(BaseSearch):
    """
    BFS search algorithm.
    
    The BFS search algorithm is a tree traversal algorithm. It starts at
    the root of the tree and explores all of the nodes at the present depth
    prior to moving onto the nodes at the next depth level.

    Args:
        BaseSearch: base class for all search algorithms.
    """
    def bfs(self) -> None:
        """
        Implements the BFS algorithm to find the shortest path from
        the source node to the destination node.
        
        Algorithm:
            1. Initialize the queue with the source node.
            2. While the queue is not empty:
                2.1. Remove the first node from the queue.
                2.2. If the node has already been visited, continue to the
                next iteration.
                2.3. If the node is not the start or end node, update its
                state.
                2.4. If the node is the end node, trace the path and return.
                2.5. For each neighbor of the node:
                    2.5.1. If the neighbor is not the start or end node, push
                    it into the queue.
        """
        start, end = self.findStartEnd()
        if not start or not end:
            return
        
        queue = [start]
        visited = set()
        parent = {start: None}

        while queue and not self._stop_event.is_set():
            current = queue.pop(0)
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
                        queue.append((nr, nc))
                        parent[(nr, nc)] = current
                        
        if not self._stop_event.is_set():
            self.noPathFound.emit()

    def startSearch(self) -> None:
        """
        Start the search algorithm.
        """
        super().startSearch(self.bfs)
