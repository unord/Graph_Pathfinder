import pygame


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
    def __init__(self, nodes, weights, draw):
        self.nodes = nodes
        self.weights = weights
        self.draw = draw

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

    def run(self):
        start_node = self.find_start()
        end_node = self.find_end()

        start_path = Path([], [], start_node, None)
        curr_paths = [start_path]
        new_paths = []

        node_cache = {start_node: start_path}
        has_changed = True

        while has_changed:
            has_changed = False

            for path in curr_paths:
                for weight in path.curr_node.weights:
                    other = weight.get_other_node(path.curr_node)
                    new_path = Path(path.nodes, path.weights, other, weight)

                    if other in node_cache:
                        if new_path.length >= node_cache[other].length:
                            continue

                    has_changed = True
                    node_cache[other] = new_path
                    new_paths.append(new_path)

            curr_paths = new_paths[:]
            new_paths.clear()
            print(curr_paths)

        print(node_cache[end_node])
