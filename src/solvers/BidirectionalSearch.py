"""
This module contains the implementation of the Bidirectional Search algorithm.
"""

import time
from collections import deque

from src.solvers.BaseSearch import BaseSearch

class BidirectionalSearch(BaseSearch):
    """
    Bidirectional search algorithm.

    Runs two BFSs in lockstep: one forward from the source, one backward
    from the destination,and stops when the two frontiers meet. For
    uniform-cost grids this is guaranteed to find a shortest path, and
    typically explores far fewer nodes than a single-source BFS.

    Args:
        BaseSearch: Base class for all search algorithms.
    """

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bidirectionalSearch(self) -> None:
        """
        Implements bidirectional BFS with proper layered expansion so the
        path returned is shortest on uniform-cost grids.

        Algorithm:
            1. Seed two frontiers: one with the source, one with the destination.
            2. Repeatedly expand whichever frontier is smaller by exactly one
               BFS layer. When adding a newly discovered node, check whether
               the other side has already reached it; if so, finish the current
               layer and then pick the meeting point that yields the shortest
               combined path.
            3. If either frontier empties before a meeting is found, no path exists.
        """
        start, end = self.findStartEnd()
        if not start or not end:
            return

        self.obstacles = self.snapshotObstacles()

        parent_start = {start: None}
        parent_end = {end: None}
        dist_start = {start: 0}
        dist_end = {end: 0}
        frontier_start = deque([start])
        frontier_end = deque([end])

        while frontier_start and frontier_end and not self._stop_event.is_set():
            # Expand the smaller frontier; if there is a tie, expand the forward side.
            if len(frontier_start) <= len(frontier_end):
                meeting = self._expandLayer(
                    frontier_start, parent_start, dist_start, parent_end, dist_end, start, end
                )
            else:
                meeting = self._expandLayer(
                    frontier_end, parent_end, dist_end, parent_start, dist_start, start, end
                )

            if meeting is not None:
                self._traceBiPath(meeting, parent_start, parent_end, start, end)
                return

        if not self._stop_event.is_set():
            self.noPathFound.emit()

    def _expandLayer(self, frontier, parents, dists, other_parents, other_dists, start, end):
        """
        Expand every node currently in `frontier` by one BFS step.

        Returns the meeting node that minimizes the combined path length over
        all intersections discovered in this layer, or None if no intersection
        was found.
        """
        best_meeting = None
        best_total = None
        # Snapshot the current layer — appends during iteration form the next layer.
        layer_size = len(frontier)
        for _ in range(layer_size):
            if self._stop_event.is_set():
                return best_meeting
            current = frontier.popleft()
            row, col = current
            if current != start and current != end:
                self.updateCellState.emit(row, col, 'checked')
            time.sleep(self.delay)

            for dr, dc in self.DIRECTIONS:
                nr, nc = row + dr, col + dc
                if not self.isFree(nr, nc):
                    continue
                neighbor = (nr, nc)
                if neighbor in parents:
                    continue
                parents[neighbor] = current
                dists[neighbor] = dists[current] + 1
                if neighbor in other_dists:
                    total = dists[neighbor] + other_dists[neighbor]
                    if best_total is None or total < best_total:
                        best_total = total
                        best_meeting = neighbor
                    # No point pushing nodes past a known meeting — any path
                    # through them is at least as long as `total`.
                    continue
                frontier.append(neighbor)
        return best_meeting

    def _traceBiPath(self, meeting, parent_start, parent_end, start, end) -> None:
        """
        Walk both parent maps outward from the meeting node to reconstruct
        the full path, then emit it cell by cell.
        """
        forward = []
        current = meeting
        while current is not None:
            forward.append(current)
            current = parent_start[current]
        forward.reverse()

        backward = []
        current = parent_end[meeting]
        while current is not None:
            backward.append(current)
            current = parent_end[current]

        for node in forward + backward:
            if self._stop_event.is_set():
                return
            row, col = node
            if node != start and node != end:
                self.updateCellState.emit(row, col, 'path')
            time.sleep(self.delay)

    def startSearch(self) -> None:
        """
        Start the search algorithm.
        """
        super().startSearch(self.bidirectionalSearch)