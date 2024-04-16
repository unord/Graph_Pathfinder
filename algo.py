import pygame

class Dijkstra:
    def __init__(self, nodes, weights, draw):
        self.nodes = nodes
        self.weights = weights
        self.draw = draw
