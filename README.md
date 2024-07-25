# path_finding_visualization
A desktop application for visualizing path finding algorithms.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Acknowledgements](#acknowledgements)
- [License](#license)
- [Notes](#notes)

## Installation
The installation process is the same on all operating systems.
To install the project on your local machine, follow these steps:
* Make sure you have Python >= 3.7 installed on your machine. You can check this by opening a terminal window and running <br />
```python3 --version``` <br />
If Python isn't installed, or the version isn't compatible, you may refer to the following [Python installation guide](https://wiki.python.org/moin/BeginnersGuide/Download)
* Install PyQt5 libraries using the Python package installer: <br />
```pip install pyqt5``` <br />
* Clone the repository: <br />
```git clone https://github.com/davidmrc6/path_finding_visualization.git```

## Usage
To run the application, navigate to the ```./path_finding_visualizer``` directory on your terminal. Then, run the `main.py` file with `python3 src/main.py`. <br />

This should open a window consisting of a grid of cells and three widgets on the top left corner of the window - a `Solve` button, a `Reset` button and a speed slider. <br />

You are first prompted to select a source (start) node and a destination (end) node by left clicking on two different cells on the grid. Furthermore, you may add obstacle cells by clicking on the right mouse button and dragging over empty cells on the grid. Finally, after setting up the grid, you can run the path finder algorithms. <br />
To run a path finding algorithm, click on the `Solve`. This will open up a selection menu containing a list of path finding algorithms. Upon selecting an algorithm, it will start running from the source node and checking the necessary cells until it finds a (not always the shortest, depending on the algorithm) path between the source node and the destination node. <br />
To change the speed at which the selected path finding algorithm checks the grid cells, you may drag the speed slider according to your preferences. <br />
You are also able to reset the grid system by clicking on the `Reset` button. <br />


## Features
* Visually following how any of the following path finding algorithms work and search for the 'optimal' path:
    * Breadth-First Search
    * Depth-First Search
    * A* Search
    * Bidirectional Search
    * Dijkstra's Algorithm
    * Greedy First-Best Search
    * Jump Point Search
    * <em>and more to come!</em>
* Setting the speed at which the line following algorithms check cells according to personal preferences
* Information about every path finding algorithm
* Path finding occurs in separate thread to the UI thread, allowing the UI to remain responsive while the algorithm runs

## Acknowledgements
* [PyQt5](https://pypi.org/project/PyQt5/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes
