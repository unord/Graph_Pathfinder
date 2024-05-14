import pygame
import sys
from uiobjects import Node, Weight, Button
from algo import BFS, AStar, Dijkstra, Greedy, DFS
from string import ascii_uppercase as alphabet
from timeline import Timeline


class Editor:
    def __init__(self, ui):
        self.ui = ui

        self.active = None
        self.consumed_names = set()

        self.nodes = self.ui.nodes
        self.weights = self.ui.weights
        self.text_input = self.ui.text_input
        self.graph_buttons = self.ui.graph_buttons
        self.algo_buttons = self.ui.algo_buttons

        self.start_marked = False
        self.end_marked = False

        self.dijkstra = Dijkstra(self.nodes, self.weights)
        self.bfs = BFS(self.nodes, self.weights)
        self.astar = AStar(self.nodes, self.weights)
        self.dfs = DFS(self.nodes, self.weights)
        self.greedy = Greedy(self.nodes, self.weights)

        self.ui.apply_callbacks(**{
            "BUTTON_GRAPH_START": self.set_node_start,
            "BUTTON_GRAPH_END": self.set_node_end,
            "BUTTON_GRAPH_DELETE": self.delete_item,
            "BUTTON_ALGO_DIJKSTRA": self.dijkstra.run,
            "BUTTON_ALGO_ASTAR": self.astar.run,
            "BUTTON_ALGO_BFS": self.bfs.run,
            "BUTTON_ALGO_DFS": self.dfs.run,
            "BUTTON_ALGO_GREEDY": self.greedy.run
        })

        self.apply_masks()

    def apply_masks(self):
        self.ui.apply_masks(**{
            "MASK_GRAPH_BUTTONS": True,
            "MASK_ALGO_BUTTONS": self.start_marked and self.end_marked,
            "MASK_TIME_BUTTONS": False
        })

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

    def add_name(self, name):
        n = self.name_to_int(name)
        self.consumed_names.add(n)

    def is_name_valid(self, name):
        if any(char not in alphabet for char in name):
            return False

        if len(name) > 3:
            return False

        if self.name_to_int(name) in self.consumed_names:
            return False

        return True

    def set_node_start(self):
        if not isinstance(self.active, Node):
            return

        if self.active.is_start:
            self.active.is_start = False
            self.start_marked = False
            self.apply_masks()
            return

        for node in self.nodes:
            node.is_start = False

        if self.active.is_end:
            self.end_marked = False

        self.active.is_start = True
        self.active.is_end = False
        self.start_marked = True

        self.apply_masks()

    def set_node_end(self):
        if not isinstance(self.active, Node):
            return

        if self.active.is_end:
            self.active.is_end = False
            self.end_marked = False
            self.apply_masks()
            return

        for node in self.nodes:
            node.is_end = False

        if self.active.is_start:
            self.start_marked = False

        self.active.is_end = True
        self.active.is_start = False
        self.end_marked = True

        self.apply_masks()

    def delete_item(self):
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

        if self.text_input.state and not self.text_input.clicked(event.pos):
            self.text_input.state = False
            return False

        if self.text_input.clicked(event.pos):
            self.text_input.state = True
            return False

        for button in self.graph_buttons:
            if button.clicked(event.pos):
                button.callback()
                return False

        for button in self.algo_buttons:
            if button.clicked(event.pos) and self.start_marked and self.end_marked:
                resp = button.callback()

                if not resp:
                    return False

                t = Timeline(self.ui, resp)
                t.main()
                self.apply_masks()
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

        # Find selected items, and check if new node is to be created
        if self.select_item(event) and event.pos[0] > 252:
            new = Node(self.ui, event.pos, self.get_next_name())
            self.nodes.append(new)
            # self.set_active(new)  # Can be enabled to set new nodes activated

    def on_keypress(self, event: pygame.event.Event) -> None:
        """
        Handle a keypress event.

        :param event: Keypress event
        :return: None
        """

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # If return key is pressed, update selected item value
        if event.key == pygame.K_RETURN:
            if isinstance(self.active, Node):
                self.text_input.user_text = self.text_input.user_text.upper()

                if self.is_name_valid(self.text_input.user_text):
                    self.remove_name(self.active.name)
                    self.active.set_name(self.text_input.user_text)
                    self.active.origin_name = self.text_input.user_text
                    self.add_name(self.active.name)

            elif isinstance(self.active, Weight):
                self.active.set_length(self.text_input.user_text)

        # If delete key is pressed, delete selected item or previous node
        elif event.key == pygame.K_DELETE:
            self.delete_item()

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
                        for weight in self.weights:
                            if weight.is_similar(self.active, node):
                                self.set_active(weight)
                                return

                        curr = Weight(self.ui, self.active, node)

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
                if hasattr(event, "pos"):
                    event.pos = self.ui.get_virtual_cords(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.set_weight(event)

            self.ui.draw()
