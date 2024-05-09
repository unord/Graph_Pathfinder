import pygame
import sys


class Timeline:
    def __init__(self, ui, timeline):
        self.ui = ui

        self.nodes = self.ui.nodes
        self.weights = self.ui.weights

        self.timeline = timeline
        self.current_pos = -1
        self.current_path = timeline[0]
        self.active_paths = []

        if not self.timeline[-1].nodes[-1].is_end:
            solution = None
            for path in self.timeline:
                if path.nodes[-1].is_end:
                    solution = path
            self.timeline.append(solution)

    def quit_func(self, event: pygame.event.Event) -> bool:
        """
        Checks event for quit-condition and exits if detected.

        :param event: Event to check
        :return: None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_BACKSPACE:
                for weight in self.weights:
                    weight.set_default()

                for node in self.nodes:
                    node.set_name_origin()

                return False
        return True

    def back(self):
        if self.current_pos < 0:
            return

        self.current_pos -= 1
        self.active_paths = self.active_paths[:-1]

        if self.active_paths:
            self.current_path = self.active_paths[-1]
        else:
            self.current_path = None

        for node in self.nodes:
            node.set_name_origin()

        for weight in self.weights:
            weight.set_default()

        for path in self.active_paths:
            for node in path.nodes:
                node.set_name(str(path.length_to_node(node)))

            for weight in path.weights:
                weight.set_searched()

        if self.current_path is not None:
            for weight in self.current_path.weights:
                weight.set_searching()

    def forward(self):
        if self.current_pos >= len(self.timeline) - 1:
            return

        self.current_pos += 1
        self.current_path = self.timeline[self.current_pos]
        self.active_paths.append(self.current_path)
        for node in self.current_path.nodes:
            node.set_name(str(self.current_path.length_to_node(node)))

        for path in self.active_paths:
            if path is not self.current_path:
                for weight in path.weights:
                    weight.set_searched()

        for weight in self.current_path.weights:
            weight.set_searching()

    def on_keypress(self, event) -> None:
        if event.key == pygame.K_LEFT:
            self.back()

        elif event.key == pygame.K_RIGHT:
            self.forward()

    def main(self) -> None:
        """
        Main function loop.

        :return: None
        """

        run = True
        while run:
            for event in pygame.event.get():
                run = self.quit_func(event)
                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
            self.ui.draw()
