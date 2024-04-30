import pygame
import sys


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
        self.current_pos = 0
        for path in self.timeline:
            for node in path.nodes:
                print(node.name)
            print("")

    def quit_func(self, event: pygame.event.Event) -> None:
        """
        Checks event for quit-condition and exits if detected.

        :param event: Event to check
        :return: None
        """

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

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

    def back(self):
        path = self.timeline[self.current_pos]

        for node in self.nodes:
            if node in path.nodes:
                if node.is_start:
                    node.set_name("0")
                else:
                    node.set_name(str(path.len_to_node(node)))
            else:
                node.set_name_origin()

    def forward(self):
        path = self.timeline[self.current_pos]

        for node in self.nodes:
            if node in path.nodes:
                if node.is_start:
                    node.set_name("0")
                else:
                    node.set_name(str(path.len_to_node(node)))

    def on_keypress(self, event) -> None:
        if event.key == pygame.K_LEFT:
            if self.current_pos > 0:
                self.current_pos -= 1
                self.back()
            
        elif event.key == pygame.K_RIGHT:

            if self.current_pos < len(self.timeline) - 1:
                self.current_pos += 1
                self.forward()


    def main(self) -> None:
        """
        Main function loop.

        :return: None
        """

        while True:
            for event in pygame.event.get():
                self.quit_func(event)
                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
            self.draw()
