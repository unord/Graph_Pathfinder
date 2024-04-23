import pygame


class Timeline:
    def __init__(self, paths, current_path, draw, window):
        self.paths = paths
        self.current_path = current_path
        self.fastest_path = None
        self.draw = draw
        self.window = window
    
    def next_path(self):
        pass

    def prev_path(self):
        pass

    def draw_path(self):
        self.draw(self.current_path)


class Path:
    def __init__(self, nodes, weights, new_node, new_weight=None):
        self.nodes = nodes[:]
        self.weights = weights[:]
        self.curr_node = new_node
        self.nodes.append(new_node)

        if new_weight is not None:
            self.weights.append(new_weight)

    @property
    def length(self):
        return sum(int(weight.length) for weight in self.weights)


class Dijkstra:
    def __init__(self, nodes, weights):
        self.nodes = nodes
        self.weights = weights

        self.fastest_paths = {}
        self.curr_paths = []
        self.new_paths = []

        self.recording = []

    def find_start(self):
        for node in self.nodes:
            if node.is_start:
                return node

        return False

    def find_end(self):
        for node in self.nodes:
            if node.is_end:
                return node

        return False

    def clear(self):
        self.fastest_paths = {}
        self.curr_paths = []
        self.new_paths = []

    def new_path(self, dest_node, path):
        self.fastest_paths[dest_node] = path
        self.new_paths.append(path)

        self.recording.append(path)

    def explore_weight(self, path, weight):
        other = weight.get_other_node(path.curr_node)
        new_path = Path(path.nodes, path.weights, other, weight)

        if other in self.fastest_paths:
            if new_path.length >= self.fastest_paths[other].length:
                return False

        self.new_path(other, new_path)
        return True

    def run(self):
        self.clear()

        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path([], [], start_node, None)
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

        return end_node in self.fastest_paths
