import pygame
from classes import Node, Weight


class Path:
    def __init__(self, new_node: Node, new_weight: Weight = None, prev_path=None):
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


class Dijkstra:
    def __init__(self, nodes: list[Node], weights: list[Weight]):
        self.nodes = nodes
        self.weights = weights

        self.fastest_paths = {}
        self.curr_paths = []
        self.new_paths = []

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
