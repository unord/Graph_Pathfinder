import pygame
from uiobjects import Node, Weight


class Path:
    def __init__(self, new_node: Node, new_weight: Weight = None, prev_path=None, heu_length: int = None):
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

        if new_weight is not None:
            self.weights.append(new_weight)
            self.length += int(new_weight.length)

        self.heu_length = 0
        if heu_length:
            self.heu_length = heu_length

    def length_to_node(self, search_node: Node) -> int | None:
        n = 0

        if search_node == self.nodes[0]:
            return 0

        for i in range(1, len(self.nodes)):
            n += int(self.weights[i - 1].length)

            if self.nodes[i] == search_node:
                return n

    @property
    def estimated_length(self):
        return self.length + self.heu_length


class Algorithm:
    def __init__(self, nodes: list[Node], weights: list[Weight]):
        self.nodes = nodes
        self.weights = weights
        self.recording = []

    def find_start(self) -> Node | bool:
        for node in self.nodes:
            if node.is_start:
                return node

        return False

    def find_end(self) -> Node | bool:
        for node in self.nodes:
            if node.is_end:
                return node

        return False


class Dijkstra(Algorithm):
    def __init__(self, nodes: list[Node], weights: list[Weight]):
        self.fastest_paths = {}
        self.curr_paths = []

        super().__init__(nodes, weights)

    def clear(self):
        self.fastest_paths = {}
        self.curr_paths = []

    def explore_path(self, path: Path, weight: Weight):
        other = weight.get_other_node(path.curr_node)
        new_path = Path(other, weight, path)

        if other in self.fastest_paths:
            if new_path.length >= self.fastest_paths[other].length:
                return

        self.fastest_paths[other] = new_path
        self.curr_paths.append(new_path)
        self.recording.append(new_path)

    def run(self):
        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path(start_node)
        self.curr_paths.append(start_path)

        self.fastest_paths[start_node] = start_path

        while self.curr_paths:
            self.curr_paths = sorted(self.curr_paths, key=lambda path: path.length, reverse=True)
            shortest_path = self.curr_paths.pop()

            for weight in shortest_path.curr_node.weights:
                self.explore_path(shortest_path, weight)

        if end_node in self.fastest_paths:
            return self.recording
        return False


class BFS(Algorithm):
    def __init__(self, nodes: list[Node], weights: list[Weight]):
        self.fastest_paths = {}
        self.curr_paths = []
        self.new_paths = []

        super().__init__(nodes, weights)

    def clear(self):
        self.fastest_paths = {}
        self.curr_paths = []
        self.new_paths = []

    def new_path(self, dest_node: Node, path: Path):
        self.fastest_paths[dest_node] = path
        self.new_paths.append(path)

        self.recording.append(path)

    def explore_weight(self, path: Path, weight: Weight) -> bool:
        other = weight.get_other_node(path.curr_node)
        new_path = Path(other, weight, path)

        if other in self.fastest_paths:
            if new_path.length >= self.fastest_paths[other].length:
                return False

        self.new_path(other, new_path)
        return True

    def run(self) -> list[Path] | bool:
        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path(start_node)
        self.curr_paths.append(start_path)

        self.fastest_paths[start_node] = start_path
        has_changed = True

        while has_changed:
            has_changed = False

            for path in self.curr_paths:
                for weight in path.curr_node.weights:
                    has_changed = self.explore_weight(path, weight) or has_changed

            self.curr_paths = self.new_paths[:]
            self.new_paths.clear()

        if end_node in self.fastest_paths:
            return self.recording
        return False


class AStar(Algorithm):
    def __init__(self, nodes: list[Node], weights: list[Weight]):
        self.curr_paths = []
        self.cand_paths = []
        self.fastest_paths = {}

        self.start_node = None
        self.end_node = None

        super().__init__(nodes, weights)

    @staticmethod
    def estimate_distance(node1: Node, node2: Node) -> int:
        diff_x = abs(node1.pos[1] - node2.pos[1])
        diff_y = abs(node1.pos[0] - node2.pos[0])
        return int((diff_x**2 + diff_y**2)**0.5) // 150

    def clear(self):
        self.curr_paths = []
        self.cand_paths = []
        self.fastest_paths = {}

        self.start_node = None
        self.end_node = None

    def find_candidates(self, path):
        for weight in path.curr_node.weights:
            other = weight.get_other_node(path.curr_node)
            new_path = Path(other, weight, path, self.estimate_distance(other, self.end_node))

            if other in self.fastest_paths:
                if new_path.length >= self.fastest_paths[other].length:
                    continue

            self.cand_paths.append(new_path)

    def run(self):
        self.clear()

        self.start_node = self.find_start()
        self.end_node = self.find_end()

        start_path = Path(self.start_node, heu_length=self.estimate_distance(self.start_node, self.end_node))
        self.curr_paths.append(start_path)
        self.find_candidates(start_path)

        self.fastest_paths[self.start_node] = start_path

        while self.end_node not in self.fastest_paths:
            self.cand_paths = sorted(self.cand_paths, key=lambda path: path.estimated_length, reverse=True)
            optimal_candidate = self.cand_paths.pop()

            if optimal_candidate.curr_node in self.fastest_paths:
                if optimal_candidate.length >= self.fastest_paths[optimal_candidate.curr_node].length:
                    continue

            self.fastest_paths[optimal_candidate.curr_node] = optimal_candidate
            self.curr_paths.append(optimal_candidate)

            self.recording.append(optimal_candidate)
            self.find_candidates(optimal_candidate)

        if self.end_node in self.fastest_paths:
            return self.recording
        return False
