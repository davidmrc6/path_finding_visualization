"""
This module contains the implementation of the Dijkstra search algorithm.
"""

import heapq
import time

from src.solvers.BaseSearch import BaseSearch

class DijkstraSearch(BaseSearch):
    """
    Dijkstra search algorithm. 
    The Dijkstra search algorithm is an extension of the BFS search algorithm
    for weighted graphs. 

    Args:
        BaseSearch: Base class for all search algorithms.
    """
    def dijkstra(self) -> None:
        """
        Implements the Dijkstra algorithm to find the shortest path from
        the source node to the destination node.

        Algorithm:
            1. Initialize the priority queue with the source node and
                initialize the distance of the source node to 0.
            2. While the priority queue is not empty:
                2.1. Remove the node with the lowest distance from the
                priority queue.
                2.2. If the node has already been visited, continue to the
                next iteration.
                2.3. If the node is not the start or end node, update its
                state.
                2.4. If the node is the end node, trace the path and return.
                2.5. For each neighbor of the node:
                    2.5.1. Calculate the distance of the neighbor.
                    2.5.2. If the distance of the neighbor is less than the
                    current distance, update the distance and push the
                    neighbor to the priority queue.
                    2.5.3. Update the parent of the neighbor.
        """
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
            
    def startSearch(self) -> None:
        """
        Start the search algorithm.
        """
        super().startSearch(self.dijkstra)
