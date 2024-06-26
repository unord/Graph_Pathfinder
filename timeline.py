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
        self.general_buttons = self.ui.general_buttons

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
            "BUTTON_TIME_STOP": self.stop,
            "BUTTON_GEN_EXIT": self.quit
        })

        self.ui.apply_masks(**{
            "MASK_GRAPH_BUTTONS": False,
            "MASK_ALGO_BUTTONS": False,
            "MASK_TIME_BUTTONS": True
        })

    @staticmethod
    def quit():
        """ Exit the program """

        pygame.quit()
        sys.exit()

    def stop(self):
        """
        Function to stop the timeline object from visualizing and return to the editor class

        :Return: None
        """

        for weight in self.weights:
            weight.set_default()

        for node in self.nodes:
            node.set_name_origin()

        self.running = False

    def back(self):
        """
        Function to visualize the previous path explored of the timeline

        :return: None
        """

        # Don't step beyond the bounds of the timeline
        if self.current_pos < 0:
            return

        # Stepping backwards, removing most recent path
        self.current_pos -= 1
        self.active_paths = self.active_paths[:-1]

        if self.active_paths:
            self.current_path = self.active_paths[-1]
        else:
            self.current_path = None

        # Reset all nodes and weights to their original
        for node in self.nodes:
            node.set_name_origin()

        for weight in self.weights:
            weight.set_default()

        # Set the length of all nodes to the shortest distance to them
        for path in self.active_paths:
            for node in path.nodes:
                length = path.length_to_node(node)

                # Faster route discovered earlier
                if node.name.isnumeric() and int(node.name) <= length:
                    continue

                node.set_name(str(length))

            # Mark searched weights as searched (red)
            for weight in path.weights:
                weight.set_searched()

        # Mark weights in current path as being searched (green)
        if self.current_path is not None:
            for weight in self.current_path.weights:
                weight.set_searching()

    def forward(self):
        """
        Function to visualize the next path of the timeline
        
        :return: None
        """

        # Don't step beyond the bounds of the timeline
        if self.current_pos >= len(self.timeline) - 1:
            return

        # Get next path in the timeline
        self.current_pos += 1
        self.current_path = self.timeline[self.current_pos]
        self.active_paths.append(self.current_path)

        # Set the length of all nodes to the shortest distance to them
        for node in self.current_path.nodes:
            length = self.current_path.length_to_node(node)

            # Faster route discovered earlier
            if node.name.isnumeric() and int(node.name) <= length:
                continue

            node.set_name(str(length))

        # Mark searched weights as searched (red)
        for path in self.active_paths:
            if path is not self.current_path:
                for weight in path.weights:
                    weight.set_searched()

        # Mark weights in current path as being searched (green)
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

        for button in self.general_buttons:
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
