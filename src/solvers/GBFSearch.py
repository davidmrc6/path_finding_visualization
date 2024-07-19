"""
This module contains the implementation of the Greedy Best First Search algorithm.
"""

import time
import heapq

from src.solvers.BaseSearch import BaseSearch

class GBFSearch(BaseSearch):
    """
    Greedy Best First Search algorithm.
    
    The Greedy Best First Search algorithm is search algorithm that 
    attempts to find the most promising path from a given starting point 
    to a goal. It prioritizes paths that appear to be the most promising, 
    regardless of whether or not they are actually the shortest path. 

    Args:
        BaseSearch: The base class for all search algorithms.
    """
    def heuristic(self, a: tuple, b: tuple) -> int:
        """
        Calculate the heuristic distance between two cells.
        
        A heuristic distance is a metric that estimates the distance
        from a given node to the goal node. In this case, the heuristic
        distance is the Manhattan distance between the two cells.

        Args:
            a (tuple): The coordinates of the first point.
            b (tuple): The coordinates of the second point.

        Returns:
            int: The heuristic distance between the two points.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def gbfs(self) -> None:
        """
        Implements the Greedy Best First Search algorithm to find the
        shortest path from the source node to the destination node.
         
        The Greedy Best First Search algorithm works by evaluating the cost
        of each possible path and then expanding the path with the lowest
        cost. The algorithm continues until it reaches the destination node
        or until it runs out of nodes to expand.
 
        Algorithm:
            1. Initialize the open set with the source node.
            2. While the open set is not empty:
                2.1. Remove the node with the lowest cost from the open set.
                2.2. If the node has already been visited, continue to the
                   next iteration.
                2.3. If the node is not the start or end node, update its
                    state.
                2.4. If the node is the end node, trace the path and return.
                2.5. For each neighbor of the node:
                    2.5.1. Calculate the cost of the neighbor.
                    2.5.2. If the cost of the neighbor is less than the current
                        cost, update the costs and push the neighbor to the
                        open set.
                    2.5.3. Update the parent of the neighbor.
        """
        start, end = self.findStartEnd()
        if not start or not end:
            return
 
        open_set = [(0, start)]
        parent = {start: None}
        visited = set()
 
        while open_set and not self._stop_event.is_set():
            # Remove the node with the lowest cost from the open set.
            current_f, current = heapq.heappop(open_set)
            row, col = current
 
            # If the node has already been visited, continue to the next iteration.
            if current in visited:
                continue
 
            visited.add(current)
            
            if current != start and current != end:
                self.updateCellState.emit(row, col, 'checked')
            time.sleep(self.delay)
 
            if current == end:
                self.tracePath(parent, end, start)
                return
 
            # Check all neighbors of current node
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                # Check that the neighbor is within the bounds of the grid.
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    # If the neighbor is not the start or end node, calculate its cost.
                    if self.cells[nr][nc].getState() in ('empty', 'end'):
                        if (nr, nc) not in visited:
                            # Calculate the cost of the neighbor.
                            neighbor_cost = self.heuristic((nr, nc), end)
                            # Update the costs and push the neighbor to the open set.
                            heapq.heappush(open_set, (neighbor_cost, (nr, nc)))
                            heapq.heappush(open_set, (self.heuristic((nr, nc), end), (nr, nc)))
                            parent[(nr, nc)] = current
                             
        # If the open set is empty, there is no path to the destination node.
        if not self._stop_event.is_set():
             self.noPathFound.emit()

    def startSearch(self) -> None:
        """
        Starts the search process.
        """
        super().startSearch(self.gbfs)
