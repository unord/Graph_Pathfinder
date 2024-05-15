import pygame
import sys
from algo import Path


class Timeline:
    """ Timeline class to manage visualisation of any algorithm. """

    def __init__(self, ui, timeline: list[Path]):
        """
        Initialize an instance of the timeline class.

        :param ui: Pointer to the ui object
        :param timeline: Each algorithm creates a timeline that this object can display
        """

        self.ui = ui

        self.nodes = self.ui.nodes
        self.weights = self.ui.weights
        self.timeline_buttons = self.ui.timeline_buttons

        self.timeline = timeline
        self.current_pos = -1
        self.current_path = timeline[0]
        self.active_paths = []

        self.running = None

        end_paths = [path for path in self.timeline if path.nodes[-1].is_end]
        solution = min(end_paths, key=lambda path: path.length)

        if not self.timeline[-1].curr_node.is_end or solution.length < self.timeline[-1].length:
            self.timeline.append(solution)

        self.ui.apply_callbacks(**{
            "BUTTON_TIME_FORWARD": self.forward,
            "BUTTON_TIME_BACK": self.back,
            "BUTTON_TIME_STOP": self.stop
        })

        self.ui.apply_masks(**{
            "MASK_GRAPH_BUTTONS": False,
            "MASK_ALGO_BUTTONS": False,
            "MASK_TIME_BUTTONS": True
        })

    def stop(self):
        for weight in self.weights:
            weight.set_default()

        for node in self.nodes:
            node.set_name_origin()

        self.running = False

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
                length = path.length_to_node(node)

                if node.name.isnumeric() and int(node.name) <= length:
                    continue

                node.set_name(str(length))

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
            length = self.current_path.length_to_node(node)

            if node.name.isnumeric() and int(node.name) <= length:
                continue

            node.set_name(str(length))

        for path in self.active_paths:
            if path is not self.current_path:
                for weight in path.weights:
                    weight.set_searched()

        for weight in self.current_path.weights:
            weight.set_searching()

    def on_click(self, event: pygame.event.Event) -> None:
        """
        Handle mouse click event.

        :param event: Mouse click event
        :return: None
        """

        for button in self.timeline_buttons:
            if button.clicked(event.pos):
                button.callback()

    def on_keypress(self, event) -> None:
        if event.key == pygame.K_LEFT:
            self.back()

        elif event.key == pygame.K_RIGHT:
            self.forward()

        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        elif event.key == pygame.K_BACKSPACE:
            self.stop()

    def main(self) -> None:
        """
        Main function loop.

        :return: None
        """

        self.running = True

        while self.running:
            for event in pygame.event.get():
                if hasattr(event, "pos"):
                    event.pos = self.ui.get_virtual_cords(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)

            self.ui.draw()
