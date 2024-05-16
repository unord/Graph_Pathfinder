from uiobjects import Node, Weight


class Path:
    """ Object to store a path and all related information """

    def __init__(self, new_node: Node, new_weight: Weight = None, prev_path=None, heu_length: int = None):
        """
        Initialize an instance of the Path class.

        :param new_node: New node added to path
        :param new_weight: New weight added to path (if any)
        :param prev_path: Path parent (if any)
        :param heu_length: Heuristic distance to target (if any)
        """

        # Initialize based on parent path if exists
        if prev_path:
            self.nodes = prev_path.nodes[:]
            self.weights = prev_path.weights[:]
            self.length = prev_path.length
        else:
            self.nodes = []
            self.weights = []
            self.length = 0

        self.curr_node = new_node
        self.nodes.append(new_node)

        # Add new weight and calculate length if exists
        if new_weight is not None:
            self.weights.append(new_weight)
            self.length += int(new_weight.length)

        # Save heuristic distance if exists
        self.heu_length = 0
        if heu_length:
            self.heu_length = heu_length

    def length_to_node(self, search_node: Node) -> int | None:
        """
        Calculate length from nodes[0] to given node.

        :param search_node: Node to find length to
        :return: Length to node or None
        """

        n = 0

        if search_node == self.nodes[0]:
            return 0

        for i in range(1, len(self.nodes)):
            n += int(self.weights[i - 1].length)

            if self.nodes[i] == search_node:
                return n

    @property
    def estimated_length(self) -> int:
        """
        Combination of real length and heuristic distance to target.

        :return: Estimated length of path to target
        """

        return self.length + self.heu_length


class Algorithm:
    """ Abstract class to derive algorithm classes from. Holds standard functions and properties. """

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        """
        Initialize an instance of the Algorithm class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        """

        self.nodes = nodes
        self.weights = weights

        # Recording stores a list of paths from the pathfinding process.
        # This is used to depict a timeline over the pathfinding process.
        self.recording = []

    def find_start(self) -> Node | None:
        """
        Find start node among nodes.

        :return: Start node or None
        """

        for node in self.nodes:
            if node.is_start:
                return node

    def find_end(self) -> Node | None:
        """
        Find end node among nodes.

        :return: End node or None
        """

        for node in self.nodes:
            if node.is_end:
                return node

    def clear(self) -> None:
        """
        Clear properties to init-state.

        :return: None
        """

        self.recording.clear()


"""class Dijkstra(Algorithm):
     Class to perform the Dijkstra pathfinding algorithm on a graph of nodes. 

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        
        Initialize an instance of the Dijkstra class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        

        # fastest_paths stores fastest found paths to all nodes in graph
        self.fastest_paths = {}

        # curr_paths stores all currently queued paths
        self.curr_paths = []

        super().__init__(nodes, weights)

    def clear(self) -> None:
        
        Clear properties to init-state.

        :return: None
        

        self.fastest_paths = {}
        self.curr_paths = []

        Algorithm.clear(self)

    def explore_path(self, path: Path, weight: Weight) -> None:
        
        Explore a path and weight for a new path.

        :param path: Path to explore
        :param weight: Weight to explore
        :return: None
        

        # If the last node is the end node, no gain will be found by further exploration
        if path.nodes[-1].is_end:
            return

        # Get path corresponding to path + weight
        other = weight.get_other_node(path.curr_node)

        # If third to last node is equal to current node, the path has repeated, discard
        if len(path.nodes) > 1 and path.nodes[-2] == other:
            return

        new_path = Path(other, weight, path)
        self.recording.append(new_path)

        if other in self.fastest_paths:

            # If a faster path to the current node exists, discard
            if new_path.length >= self.fastest_paths[other].length:
                return

            # New path is the fastest, remove redundant paths from curr_paths
            self.curr_paths = list(filter(lambda path: path.nodes[-1] != other, self.curr_paths))

        # New paths passes checks, add it to list
        self.fastest_paths[other] = new_path
        self.curr_paths.append(new_path)

    def run(self) -> list[Path] | None:
        
        Run the pathfinding algorithm.

        :return: Recording of pathfinding or None
        

        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path(start_node)
        self.curr_paths.append(start_path)

        self.fastest_paths[start_node] = start_path

        # While unexplored paths exist, repeat
        while self.curr_paths:

            # Get path with shortest length to start-node
            self.curr_paths = sorted(self.curr_paths, key=lambda path: path.length, reverse=True)
            shortest_path = self.curr_paths.pop()

            # Explore all weights connected to shortest path
            for weight in shortest_path.curr_node.weights:
                self.explore_path(shortest_path, weight)

        if end_node in self.fastest_paths:
            return self.recording"""


class Dijkstra(Algorithm):
    """ Class to perform the Dijkstra pathfinding algorithm on a graph of nodes. """

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        """
        Initialize an instance of the Dijkstra class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        """

        # fastest_paths stores fastest found paths to all nodes in graph
        self.fastest_paths = {}

        # curr_paths stores all currently queued paths
        self.cand_paths = []

        super().__init__(nodes, weights)

    def clear(self) -> None:
        """
        Clear properties to init-state.

        :return: None
        """

        self.fastest_paths = {}
        self.cand_paths.clear()

        Algorithm.clear(self)

    def find_candidates(self, path: Path) -> None:
        """
        Explore path to find candidate paths.

        :param path: Path to explore
        :return: None
        """

        for weight in path.curr_node.weights:
            other = weight.get_other_node(path.curr_node)
            new_path = Path(other, weight, path)

            # If path is longer than known path, discard
            if new_path.curr_node in self.fastest_paths:
                if new_path.length >= self.fastest_paths[new_path.curr_node].length:
                    continue

            self.cand_paths.append(new_path)

    def run(self) -> list[Path] | None:
        """
        Run the pathfinding algorithm.

        :return: Recording of pathfinding or None
        """

        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path(start_node)
        self.find_candidates(start_path)
        self.fastest_paths[start_node] = start_path

        # Repeat until end-node is found
        while end_node not in self.fastest_paths:

            # Select node with lowest estimated length
            self.cand_paths = sorted(self.cand_paths, key=lambda path: path.estimated_length, reverse=True)
            optimal_candidate = self.cand_paths.pop()
            self.recording.append(optimal_candidate)

            # If path is longer than known path, discard
            if optimal_candidate.curr_node in self.fastest_paths:
                if optimal_candidate.length >= self.fastest_paths[optimal_candidate.curr_node].length:
                    continue

            # Save path and find candidates
            self.fastest_paths[optimal_candidate.curr_node] = optimal_candidate
            self.find_candidates(optimal_candidate)

        if end_node in self.fastest_paths:
            return self.recording


class BFS(Algorithm):
    """ Class to perform the BFS pathfinding algorithm on a graph of nodes. """

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        """
        Initialize an instance of the BFS class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        """

        # fastest_paths stores fastest found paths to all nodes in graph
        self.fastest_paths = {}

        # curr_paths stores all currently queued paths
        self.curr_paths = []

        # new_paths stores all paths generated during current round of exploration
        self.new_paths = []

        super().__init__(nodes, weights)

    def clear(self) -> None:
        """
        Clear properties to init-state.

        :return: None
        """

        self.fastest_paths = {}
        self.curr_paths.clear()
        self.new_paths.clear()

        Algorithm.clear(self)

    def explore_weight(self, path: Path, weight: Weight) -> None:
        """
        Explore a path and weight for a new path.

        :param path: Path to explore
        :param weight: Weight to explore
        :return: None
        """

        # If the last node is the end node, no gain will be found by further exploration
        if path.nodes[-1].is_end:
            return

        # Get path corresponding to path + weight
        other = weight.get_other_node(path.curr_node)

        # If third to last node is equal to current node, the path has repeated, discard
        if len(path.nodes) > 1 and path.nodes[-2] == other:
            return

        new_path = Path(other, weight, path)
        self.recording.append(new_path)

        if other in self.fastest_paths:

            # If a faster path to the current node exists, discard
            if new_path.length >= self.fastest_paths[other].length:
                return

            # New path is the fastest, remove redundant paths from curr_paths
            self.curr_paths = list(filter(lambda path: path.nodes[-1] != other, self.curr_paths))

        # New paths passes checks, add it to list
        self.fastest_paths[other] = new_path
        self.new_paths.append(new_path)

    def run(self) -> list[Path] | None:
        """
        Run the pathfinding algorithm.

        :return: Recording of pathfinding or None
        """

        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path(start_node)
        self.new_paths.append(start_path)

        self.fastest_paths[start_node] = start_path

        # While new and faster paths are being found
        while self.new_paths:

            # Transfer new paths to current paths (breadth first)
            self.curr_paths = self.new_paths[:]
            self.new_paths.clear()

            # Explore all weights of all paths
            for path in self.curr_paths:
                for weight in path.curr_node.weights:
                    self.explore_weight(path, weight)

        if end_node in self.fastest_paths:
            return self.recording


class AStar(Algorithm):
    """
    Class to perform the A-Star pathfinding algorithm on a graph of nodes.

    Important note: This algorithm is not guaranteed (though usually expected) to return the fastest path.
    This is because, the heuristic in use is imperfect and can be deceived.
    """

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        """
        Initialize an instance of the AStar class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        """

        # fastest_paths stores fastest found paths to all nodes in graph
        self.fastest_paths = {}

        # cand_paths stores candidate paths in the queue
        self.cand_paths = []

        self.start_node = None
        self.end_node = None

        super().__init__(nodes, weights)

    @staticmethod
    def estimate_distance(node1: Node, node2: Node) -> int:
        """
        Estimate distance between two nodes. Basic heuristic function.

        :param node1: Node 1
        :param node2: Node 2
        :return: Estimated distance between nodes
        """

        diff_x = abs(node1.pos[1] - node2.pos[1])
        diff_y = abs(node1.pos[0] - node2.pos[0])
        return int((diff_x**2 + diff_y**2)**0.5) // 120

    def clear(self) -> None:
        """
        Clear properties to init-state.

        :return: None
        """

        self.cand_paths.clear()
        self.fastest_paths = {}

        self.start_node = None
        self.end_node = None

        Algorithm.clear(self)

    def find_candidates(self, path: Path) -> None:
        """
        Explore path to find candidate paths.

        :param path: Path to explore
        :return: None
        """

        for weight in path.curr_node.weights:
            other = weight.get_other_node(path.curr_node)
            new_path = Path(other, weight, path, self.estimate_distance(other, self.end_node))

            # If path is longer than known path, discard
            if new_path.curr_node in self.fastest_paths:
                if new_path.length >= self.fastest_paths[new_path.curr_node].length:
                    continue

            self.cand_paths.append(new_path)

    def run(self) -> list[Path] | None:
        """
        Run the pathfinding algorithm.

        :return: Recording of pathfinding or None
        """

        self.clear()

        self.start_node = self.find_start()
        self.end_node = self.find_end()

        start_path = Path(self.start_node, heu_length=self.estimate_distance(self.start_node, self.end_node))
        self.find_candidates(start_path)
        self.fastest_paths[self.start_node] = start_path

        # Repeat until end-node is found
        while self.end_node not in self.fastest_paths:

            # Select node with lowest estimated length
            self.cand_paths = sorted(self.cand_paths, key=lambda path: path.estimated_length, reverse=True)
            optimal_candidate = self.cand_paths.pop()
            self.recording.append(optimal_candidate)

            # If path is longer than known path, discard
            if optimal_candidate.curr_node in self.fastest_paths:
                if optimal_candidate.length >= self.fastest_paths[optimal_candidate.curr_node].length:
                    continue

            # Save path and find candidates
            self.fastest_paths[optimal_candidate.curr_node] = optimal_candidate
            self.find_candidates(optimal_candidate)

        if self.end_node in self.fastest_paths:
            return self.recording


class DFS(Algorithm):
    """
    Class to perform the DFS pathfinding algorithm on a graph of nodes.

    Important note: This algorithm is not guaranteed (or expected) to find the fastest path.
    It will return the first path to the end-node it finds. This is the case,
    because a depth-first search gives no good exit-condition to go by.
    As such, the algorithm would have to exhaust all possible paths to find the fastest.
    """

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        """
        Initialize an instance of the AStar class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        """

        # fastest_paths stores fastest found paths to all nodes in graph
        self.fastest_paths = {}

        # curr_paths stores all currently queued paths
        self.curr_paths = []

        super().__init__(nodes, weights)

    def clear(self) -> None:
        """
        Clear properties to init-state.

        :return: None
        """

        self.curr_paths.clear()
        self.fastest_paths = {}

        Algorithm.clear(self)

    def explore_path(self, path: Path, weight: Weight) -> bool:
        """
        Explore a path and weight.

        :param path: Path to explore
        :param weight: Weight to explore
        :return: Whether end node has been found
        """

        # Get path corresponding to path + weight
        other = weight.get_other_node(path.curr_node)

        # If third to last node is equal to current node, the path has repeated, discard
        if len(path.nodes) > 1 and path.nodes[-2] == other:
            return False

        new_path = Path(other, weight, path)
        self.recording.append(new_path)

        if other in self.fastest_paths:

            # If path is slower than known path, discard
            if new_path.length >= self.fastest_paths[other].length:
                return False

            # Filter redundant paths from curr_paths
            self.curr_paths = list(filter(lambda path: path.nodes[-1] != other, self.curr_paths))

        self.fastest_paths[other] = new_path

        # Push new path to top of stack (depth first)
        self.curr_paths.insert(0, new_path)

        return other.is_end

    def run(self) -> list[Path] | None:
        """
        Run the pathfinding algorithm.

        :return: Recording of pathfinding or None
        """

        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path(start_node)
        self.curr_paths.append(start_path)

        ending_found = False

        # Iterate until ending found or no more paths to explore
        while not ending_found and self.curr_paths:

            # Get path from top of stack
            cand_path = self.curr_paths.pop(0)

            for weight in cand_path.curr_node.weights:
                if self.explore_path(cand_path, weight):
                    ending_found = True
                    break

        if end_node in self.fastest_paths:
            return self.recording


class Greedy(Algorithm):
    """
    Class to perform the greedy pathfinding algorithm on a graph of nodes.

    Important note: This algorithm is not guaranteed (or expected) to find the fastest path.
    It relies solely on heuristic, and therefore doesn't consider current path length, only distance to target.
    """

    def __init__(self, nodes: list[Node], weights: list[Weight]):
        """
        Initialize an instance of the Greedy class.

        :param nodes: Nodes in graph
        :param weights: Weights in graph
        """

        # fastest_paths stores fastest found paths to all nodes in graph
        self.fastest_paths = {}

        # cand_paths stores candidate paths in the queue
        self.cand_paths = []

        self.start_node = None
        self.end_node = None

        super().__init__(nodes, weights)

    @staticmethod
    def estimate_distance(node1: Node, node2: Node) -> int:
        """
        Estimate distance between two nodes. Basic heuristic function.

        :param node1: Node 1
        :param node2: Node 2
        :return: Estimated distance between nodes
        """

        diff_x = abs(node1.pos[1] - node2.pos[1])
        diff_y = abs(node1.pos[0] - node2.pos[0])
        return int((diff_x**2 + diff_y**2)**0.5) // 120

    def clear(self) -> None:
        """
        Clear properties to init-state.

        :return: None
        """

        self.cand_paths.clear()
        self.fastest_paths = {}

        self.start_node = None
        self.end_node = None

        Algorithm.clear(self)

    def find_candidates(self, path: Path) -> None:
        """
        Explore path to find candidate paths.

        :param path: Path to explore
        :return: None
        """

        for weight in path.curr_node.weights:
            other = weight.get_other_node(path.curr_node)
            new_path = Path(other, weight, path, self.estimate_distance(other, self.end_node))
            self.cand_paths.append(new_path)

    def run(self) -> list[Path] | None:
        """
        Run the pathfinding algorithm.

        :return: Recording of pathfinding or None
        """

        self.clear()

        self.start_node = self.find_start()
        self.end_node = self.find_end()

        start_path = Path(self.start_node, heu_length=self.estimate_distance(self.start_node, self.end_node))
        self.find_candidates(start_path)
        self.fastest_paths[self.start_node] = start_path

        # Repeat until end-node is found
        while self.end_node not in self.fastest_paths:

            # Select node with smallest heuristic distance to target
            self.cand_paths = sorted(self.cand_paths, key=lambda path: path.heu_length, reverse=True)
            optimal_candidate = self.cand_paths.pop()
            self.recording.append(optimal_candidate)

            # If path is slower than known path, discard
            if optimal_candidate.curr_node in self.fastest_paths:
                if optimal_candidate.length >= self.fastest_paths[optimal_candidate.curr_node].length:
                    continue

            self.fastest_paths[optimal_candidate.curr_node] = optimal_candidate
            self.find_candidates(optimal_candidate)

        if self.end_node in self.fastest_paths:
            return self.recording
