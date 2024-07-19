"""
This module contains the implementation of the Bidirectional Search algorithm.
"""

import time

from src.solvers.BaseSearch import BaseSearch

class BidirectionalSearch(BaseSearch):
    """
    Bidirectional search algorithm.
    
    Bidirectional Search is a graph search algorithm which finds the shortest
    path between a specified source node and a specified destination node (in a directed graph).
    It runs two simultaenous searches, one forward from the source node, and one backward from 
    the destination node. 

    Args:
        BaseSearch: Base class for all search algorithms.
    """
    def bidirectionalSearch(self):
        """
        Implements the Bidirectional Search algorithm to find the shortest path
        from the source node to the destination node.

        Algorithm:
            1. Initialize two queues - one starting from the source node
            and one starting from the destination node.
            2. While both queues are not empty:
                2.1. Remove the first node from the start queue.
                2.2. If the node has already been visited, continue to the
                next iteration.
                2.3. If the node is not the start or end node, update its
                state.
                2.4. If the node is the end node, trace the path and return.
                2.5. For each neighbor of the node:
                    2.5.1. If the neighbor is not the start or end node, push
                    it into the queue.
                2.6 Repeat the same process for the end queue.
            3. Trace the path from the queue which has the least number of
            nodes.
        """
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
            while current and not self._stop_event.is_set():
                path_start.append(current)
                current = parent_start[current]
            current = meeting_point
            while current and not self._stop_event.is_set():
                path_end.append(current)
                current = parent_end[current]
            full_path = path_start[::-1] + path_end[1:]
            for node in full_path:
                if self._stop_event.is_set():
                    return
                row, col = node
                if node != start and node != end:
                    self.updateCellState.emit(row, col, 'path')
                time.sleep(0.1)

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
                            time.sleep(self.delay)

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
                            time.sleep(self.delay)

        if not self._stop_event.is_set():
            self.noPathFound.emit()

    def startSearch(self):
        """
        Start the search algorithm.
        """
        super().startSearch(self.bidirectionalSearch)
