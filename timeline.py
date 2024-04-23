import pygame


class Timeline:
    def __init__(self, window, ui, timeline):
        self.bg_color = (100, 100, 240, 0.5)
        self.window = window
        self.ui = ui

        self.nodes = self.ui.nodes
        self.weights = self.ui.weights
        self.text_input = self.ui.text_input
        self.buttons = self.ui.buttons
        self.algo_buttons = self.ui.algo_buttons

        self.timeline = timeline
        print(self.timeline)

    def draw(self) -> None:
        """
        Draw the scene.

        :return: None
        """

        self.window.fill(self.bg_color)

        for weight in self.weights:
            weight.draw(self.window)

        for node in self.nodes:
            node.draw(self.window)

        for button in self.buttons:
            button.draw(self.window)

        for button in self.algo_buttons:
            button.draw(self.window)

        self.text_input.draw(self.window)
        pygame.display.update()

    def main(self) -> None:
        """
        Main function loop.

        :return: None
        """

        while True:

            self.draw()
