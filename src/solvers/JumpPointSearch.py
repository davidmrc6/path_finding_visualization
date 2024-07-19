""""
This module contains the implementation of the Jump Point Search algorithm.
"""

import time
import heapq

from src.solvers.BaseSearch import BaseSearch

class JumpPointSearch(BaseSearch):
    """
    Jump Point Search algorithm.

    This class implements the Jump Point Search algorithm for solving the
    pathfinding problem on a uniform-cost grid.

    Attributes:
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
 
    def jump(self, current: tuple, direction: tuple, end: tuple) -> tuple:
        """
        Jump to the next cell in a given direction.

        Args:
            current (tuple): The current cell coordinates.
            direction (tuple): The direction to jump in.
            end (tuple): The end cell coordinates.

        Returns:
            tuple or None: The next cell coordinates if jump is valid, None otherwise.
        """
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
 
    def identifySuccessors(self, current: tuple, end: tuple) -> list:
        """
        Identify the successors of a given cell.

        Args:
            current (tuple): The current cell coordinates.
            end (tuple): The end cell coordinates.

        Returns:
            list: The list of successors.
        """
        successors = []
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            jump_point = self.jump(current, direction, end)
            if jump_point:
                successors.append(jump_point)
        return successors
 
    def jps(self):
        """
        Perform the Jump Point Search algorithm.

        This method implements the Jump Point Search algorithm for solving
        the pathfinding problem on a uniform-cost grid.
        """
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
        """
         Start the search algorithm.
        """
        super().startSearch(self.jps)
