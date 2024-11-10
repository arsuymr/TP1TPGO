# TP1TPGO

## Articulation Points Calculation in Unoriented Graph

### Description
This program implements an algorithm to calculate **articulation points** (also known as **cut vertices**) in an **unoriented graph**. Articulation points are vertices in a graph whose removal increases the number of connected components. The program utilizes **Depth-First Search (DFS)** to find these points in the graph.

### Key Concepts
- **Articulation Points**: Vertices whose removal disconnects the graph, increasing the number of connected components.
- **Depth-First Search (DFS)**: A graph traversal algorithm used to explore nodes and edges. DFS is used here to identify articulation points.
- **Unoriented Graph**: A graph where edges do not have a direction (undirected edges).

### How It Works
1. **Graph Creation**: The program allows the user to create a graph by specifying the number of vertices and adding edges between them.
2. **DFS Traversal**: The program uses a DFS-based algorithm to explore the graph and identify articulation points.
3. **Articulation Points Identification**: The DFS traversal keeps track of discovery and low times to determine if a vertex is an articulation point.
4. **Disconnected Graph Detection**: If the graph is disconnected, the program notifies the user that it cannot calculate articulation points.

### Features
- **Graph Creation**: Create an undirected graph by specifying vertices and edges.
- **Articulation Point Calculation**: Calculate and display the articulation points in the graph.
- **Graph Visualization**: Display the graph using Matplotlib, marking articulation points.
- **User Notifications**: Display feedback messages about actions (e.g., adding edges, calculating points).
- **Disconnection Detection**: Alerts the user if the graph is not connected.

### Requirements
- Python 3.x
- `networkx` (for graph manipulation and algorithms)
- `matplotlib` (for graph visualization)
- `tkinter` (for graphical user interface)

### Installation
To run this program, you will need to install the required libraries. You can do this with the following command:

```bash
pip install networkx matplotlib
