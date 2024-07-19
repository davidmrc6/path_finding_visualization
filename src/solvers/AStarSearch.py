"""
This module contains the implementation of the A* search algorithm.
"""

import time
import heapq

from src.solvers.BaseSearch import BaseSearch

class AStarSearch(BaseSearch):
    """
    A* search algorithm.
    
    The A* search algorithm is an extension of Dijkstra's algorithm.
    It achieves better performance by using heuristics to guide its search.

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

    def astar(self) -> None:
        """
        Implements the A* algorithm to find the shortest path from
        the source node to the destination node.
        
        Algorithm:
            1. Initialize the open set with the source node and initialize
                the g_cost and f_cost of the source node to 0.
            2. While the open set is not empty:
                2.1. Select the node with the lowest f_cost from the open set.
                2.2. If the node has already been visited, continue to the
                next iteration.
                2.3. If the node is not the start or end node, update its
                state.
                2.4. If the node is the end node, trace the path and return.
                2.5. For each neighbor of the node:
                    2.5.1. Calculate the g_cost of the neighbor.
                    2.5.2. If the g_cost of the neighbor is less than the current
                    g_cost, update the g_costs and f_costs.
                    2.5.3. Push the neighbor to the open set with its f-cost.
                    2.5.4. Update the parent of the neighbor.
                    
        Notes:
            - The g_cost is the cost of reaching a node from the starting node
            - The f_cost stands for the total cost of reaching a node from the starting
            node and then reaching the goal node. The f_cost is the sum of the g_cost
            and the heuristic cost of the current node to the goal node.
        """
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

            # if end node is reached, trace path and return
            if current == end:
                self.tracePath(parent, end, start)
                return

            # Check neighbors of current cell
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.cells[nr][nc].getState() in ('empty', 'end'):
                        tentative_g_cost = g_costs[current] + 1  # Assuming uniform cost
                        if (nr, nc) not in g_costs or tentative_g_cost < g_costs[(nr, nc)]:
                            # Update g_cost and f_cost
                            g_costs[(nr, nc)] = tentative_g_cost
                            f_cost = tentative_g_cost + self.heuristic((nr, nc), end)
                            f_costs[(nr, nc)] = f_cost
                            heapq.heappush(open_set, (f_cost, (nr, nc)))
                            parent[(nr, nc)] = current
                            
        if not self._stop_event.is_set():
            self.noPathFound.emit()

    def startSearch(self):
        """
        Start the search algorithm.
        """
        super().startSearch(self.astar)