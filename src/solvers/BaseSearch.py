"""
This module contains the BaseSearch class which is the base class for all search algorithms.
"""

import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class BaseSearch(QObject):
    """
    Base class for all search algorithms.
    
    The BaseSearch class contains all methods which are shared by all
    search algorithms. The class is inherited by all search algorithms
    and provides a common interface for starting, stopping and checking
    the status of the search algorithms.

    Attributes:
        gridWidget (GridWidget): The grid widget object.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        cells (list): The 2D list of cells in the grid.
        _stop_event (threading.Event): The event object to stop the search.
        delay (float): The delay between cell updates.
    """
    
    updateCellState = pyqtSignal(int, int, str)
    noPathFound = pyqtSignal()

    def __init__(self, gridWidget) -> None:
        super().__init__()
        self.gridWidget = gridWidget
        self.rows = gridWidget.rows
        self.cols = gridWidget.cols
        self.cells = gridWidget.cells
        self._stop_event = threading.Event()
        self.delay = 0.05

    def setDelay(self, speed) -> None:
        """
        Set the delay between cell updates.

        Args:
            speed: The speed of the search algorithm.
        """
        self.delay = 1 / speed

    def findStartEnd(self) -> tuple:
        """
        Find the start and end cells in the grid.

        Returns:
            tuple: The row and column indices of the start and end cells.
        """
        start = end = None
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].getState() == 'start':
                    start = (row, col)
                elif self.cells[row][col].getState() == 'end':
                    end = (row, col)
        return start, end

    def tracePath(self, parent, end, start) -> None:
        """
        Trace the path from the end cell to the start cell

        Args:
            parent (dict): A dictionary mapping each cell to its predecessor 
                       in the path, used to reconstruct the path.
            end (tuple): Coordinates of the end cell (row, col).
            start (tuple): Coordinates of the start cell (row, col).
        """
        current = end
        while current and not self._stop_event.is_set():
            row, col = current
            if current != end and current != start:
                self.updateCellState.emit(row, col, 'path')
            current = parent[current]
            time.sleep(0.1)

    def startSearch(self, algorithm) -> None:
        """
        Start the search algorithm in a separate thread.

        Args:
            algorithm (Callable): The search function to be executed in a new thread.
        """
        self._stop_event.clear()
        self.search_thread = threading.Thread(target=algorithm)
        self.search_thread.start()

    def stopSearch(self) -> None:
        """
        Stop the search algorithm by setting the stop event
            and joining the search thread if it is alive.
        """
        self._stop_event.set()
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join()

    def isRunning(self) -> bool:
        """
        Check if the search algorithm is currently running.

        Returns:
            bool: True if the search thread is alive, otherwise False.
        """
        return self.search_thread and self.search_thread.is_alive()
