import pygame
import ctypes
import sys
from classes import Node, TextInput, Weight, Button
from algo import Dijkstra
from string import ascii_uppercase as alphabet


class UI:
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        self.bg_color = (100, 100, 240, 0.5)
        self.info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = self.info.current_w, self.info.current_h

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags=pygame.FULLSCREEN)
        pygame.display.set_caption('Graph Visualizer')
        self.text_input = TextInput()

        self.buttons = []
        self.nodes = []
        self.weights = []

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

        self.text_input.draw(self.window)
        pygame.display.update()


class Game:
    def __init__(self):
        self.active = None
        self.consumed_names = set()

        self.ui = UI()
        self.nodes = self.ui.nodes
        self.weights = self.ui.weights
        self.buttons = self.ui.buttons
        self.text_input = self.ui.text_input

        self.dijkstra = Dijkstra(self.nodes, self.weights)

        self.buttons.append(Button(pygame.Rect(400, 200, 140, 32), "start", self.set_node_start))
        self.buttons.append(Button(pygame.Rect(600, 200, 140, 32), "end", self.set_node_end))
        self.buttons.append(Button(pygame.Rect(800, 200, 140, 32), "dijkstra", self.dijkstra.run))
    
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

    @staticmethod
    def int_to_name(n):
        digits = []

        while n:
            n -= 1
            digits.append(alphabet[n % len(alphabet)])
            n //= len(alphabet)

        digits = digits[::-1]
        return "".join(digits)

    @staticmethod
    def name_to_int(name):
        n = 0

        for i, char in enumerate(name[::-1]):
            idx = alphabet.index(char)
            n += (idx + 1) * (26 ** i)

        return n

    def get_next_name(self):
        i = 1

        while True:
            if i not in self.consumed_names:
                self.consumed_names.add(i)
                return self.int_to_name(i)

            i += 1

    def remove_name(self, name):
        n = self.name_to_int(name)

        if n in self.consumed_names:
            self.consumed_names.remove(n)

    def is_name_valid(self, name):
        if any(char not in alphabet for char in name):
            return False

        elif self.name_to_int(name) in self.consumed_names:
            return False

        return True

    def set_node_start(self):
        if not isinstance(self.active, Node):
            return

        if self.active.is_start:
            self.active.is_start = False
            return

        for node in self.nodes:
            node.is_start = False

        self.active.is_start = True
        self.active.is_end = False

    def set_node_end(self):
        if not isinstance(self.active, Node):
            return

        if self.active.is_end:
            self.active.is_end = False
            return

        for node in self.nodes:
            node.is_end = False

        self.active.is_end = True
        self.active.is_start = False

    def set_active(self, new: Node | Weight | Button | None) -> None:
        """
        Sets the active item and handles necessary changes involved in the process.

        :param new: Item to set as active
        :return: None
        """

        # Unset state of old active item
        if self.active:
            self.active.state = False

        self.active = new

        # If new item is not None, set its state
        if self.active is not None:
            self.active.state = True

        # Update the text input appropriately
        if self.active is None:
            self.text_input.user_text = ""
        elif isinstance(self.active, Node):
            self.text_input.user_text = self.active.name
        elif isinstance(self.active, Weight):
            self.text_input.user_text = self.active.length

    def select_item(self, event: pygame.event.Event) -> bool:
        """
        Checks all items for clicks and evaluates whether the conditions for creating a new node is met.

        :param event: Event to be evaluated
        :return: Whether a new node should be created
        """

        for button in self.buttons:
            if button.clicked(event.pos):
                return False

        # Iterate all nodes and detect presses
        for node in self.nodes:
            if node.clicked(event.pos):
                self.set_active(node)
                return False

        # Iterate all weights and detect presses
        for weight in self.weights:
            if weight.clicked(event.pos):
                self.set_active(weight)
                return False

        # If active is already None, new node should be created
        res = self.active is None
        self.set_active(None)
        return res

    def on_click(self, event: pygame.event.Event) -> None:
        """
        Handle mouse click event.

        :param event: Mouse click event
        :return: None
        """

        # Ensure text input field is not clicked
        self.text_input.clicked(event)
        if not self.text_input.state:

            # Find selected items, and check if new node is to be created
            if self.select_item(event):
                new = Node(event, self.get_next_name())
                self.nodes.append(new)
                # self.set_active(new)  # Can be enabled to set new nodes activated
    
    def on_keypress(self, event: pygame.event.Event) -> None:
        """
        Handle a keypress event.

        :param event: Keypress event
        :return: None
        """

        # If return key is pressed, update selected item value
        if event.key == pygame.K_RETURN:
            if isinstance(self.active, Node):
                if self.is_name_valid(self.text_input.user_text):
                    self.active.set_name(self.text_input.user_text)

            elif isinstance(self.active, Weight):
                self.active.set_length(self.text_input.user_text)

        # If delete key is pressed, delete selected item or previous node
        elif event.key == pygame.K_DELETE:

            # Selected item is a weight
            if isinstance(self.active, Weight):
                self.weights.remove(self.active)

                # Ensure nodes are updated to not include references to weight
                for node in self.nodes:
                    node.remove_weight(self.active)

                self.set_active(None)
                return

            # Selected item is a node
            elif isinstance(self.active, Node):
                deleted = self.active
                self.nodes.remove(self.active)
                self.set_active(None)

            else:
                deleted = self.nodes.pop()

            self.remove_name(deleted.name)

            # Delete all connected weights and update nodes accordingly
            for weight in deleted.weights:
                for node in self.nodes:
                    node.remove_weight(weight)

                self.weights.remove(weight)

        else:

            # Input falls through to text input (if state is set)
            self.text_input.input(event)

    def set_weight(self, event: pygame.event.Event) -> None:
        """
        Creates a new weight if the user has dragged mouse between nodes.

        :param event: Mouse button up event to be evaluated
        :return: None
        """

        # Check is node is currently selected
        if isinstance(self.active, Node):
            for node in self.nodes:
                if node is not self.active:

                    # Find node that user unclicked on (dragged)
                    if node.clicked(event.pos):
                        curr = Weight(self.active, node)

                        # Add new weight to both connected nodes
                        self.active.add_weight(curr)
                        node.add_weight(curr)

                        self.set_active(curr)
                        self.weights.append(curr)

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.set_weight(event)

            self.ui.draw()


if __name__ == "__main__":
    game = Game()
    game.main()
