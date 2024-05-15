import pygame
import sys
from uiobjects import Node, Weight
from algo import BFS, AStar, Dijkstra, Greedy, DFS
from string import ascii_uppercase as alphabet
from timeline import Timeline


class Editor:
    """ Editor class that allows the user to create and edit graphs """

    def __init__(self, ui):
        """
        Create an instance of the Editor class.

        :param ui: Pointer to the ui object
        """

        self.ui = ui

        # active stores currently selected UI-object
        self.active = None
        self.consumed_names = set()

        # Copy references to UI objects
        self.nodes = self.ui.nodes
        self.weights = self.ui.weights
        self.text_input = self.ui.text_input
        self.graph_buttons = self.ui.graph_buttons
        self.algo_buttons = self.ui.algo_buttons

        self.start_marked = False
        self.end_marked = False

        # Create algo objects with references to node and weight lists
        self.dijkstra = Dijkstra(self.nodes, self.weights)
        self.bfs = BFS(self.nodes, self.weights)
        self.astar = AStar(self.nodes, self.weights)
        self.dfs = DFS(self.nodes, self.weights)
        self.greedy = Greedy(self.nodes, self.weights)

        # Apply function callbacks
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

    def apply_masks(self) -> None:
        """
        Update mask states.

        :return: None
        """

        self.ui.apply_masks(**{
            "MASK_GRAPH_BUTTONS": True,
            "MASK_ALGO_BUTTONS": self.start_marked and self.end_marked,
            "MASK_TIME_BUTTONS": False
        })

    """
    The editor supports automatically naming nodes. These will be named alphabetically and in order. Example:
        0: A
        1: B
        ...
        26: Z
        27: AA
        28: AB
    """

    @staticmethod
    def int_to_name(n: int) -> str:
        """
        Convert a number to its alphabetical representation.

        :param n: Number to represent
        :return: Alphabetic representation
        """

        digits = []

        while n:
            n -= 1
            digits.append(alphabet[n % len(alphabet)])
            n //= len(alphabet)

        digits = digits[::-1]
        return "".join(digits)

    @staticmethod
    def name_to_int(name: str) -> int:
        """
        Convert an alphabetical representation to a number.

        :param name: Alphabetic representation
        :return: Equivalent number
        """

        n = 0

        for i, char in enumerate(name[::-1]):
            idx = alphabet.index(char)
            n += (idx + 1) * (26 ** i)

        return n

    def get_next_name(self) -> str:
        """
        Find next available name, such that two nodes don't have the same name.

        :return: Alphabetic representation
        """

        i = 1

        while True:
            if i not in self.consumed_names:
                self.consumed_names.add(i)
                return self.int_to_name(i)

            i += 1

    def remove_name(self, name: str) -> None:
        """
        Remove name from consumed_names, freeing the name to be used by other nodes.

        :param name: Alphabetic representation
        :return: None
        """

        n = self.name_to_int(name)

        if n in self.consumed_names:
            self.consumed_names.remove(n)

    def add_name(self, name: str) -> None:
        """
        Add name to consumed_names, marking it as already in use.

        :param name: Alphabetic representation
        :return: None
        """

        n = self.name_to_int(name)
        self.consumed_names.add(n)

    def is_name_valid(self, name: str) -> bool:
        """
        Check whether given name is valid to use.

        :param name: Alphabetic representation
        :return: Whether name is valid
        """

        # Ensure all characters in name are apart of the alphabet
        if any(char not in alphabet for char in name):
            return False

        # No need to support long names (18278 valid names)
        if len(name) > 3:
            return False

        # Ensure name isn't already in use
        if self.name_to_int(name) in self.consumed_names:
            return False

        return True

    def set_node_start(self) -> None:
        """
        Set currently selected node as start of graph.

        :return: None
        """

        # Ensure selected object is a node
        if not isinstance(self.active, Node):
            return

        # If currently selected node is already start, unset the state
        if self.active.is_start:
            self.active.is_start = False
            self.start_marked = False
            self.apply_masks()
            return

        # Unset state for all other nodes (only one start node)
        for node in self.nodes:
            node.is_start = False

        # If current node is already end, unset the state
        if self.active.is_end:
            self.end_marked = False

        self.active.is_start = True
        self.active.is_end = False
        self.start_marked = True

        self.apply_masks()

    def set_node_end(self) -> None:
        """
        Set currently selected node as end of graph.

        :return: None
        """

        # Ensure selected object is a node
        if not isinstance(self.active, Node):
            return

        # If currently selected node is already end, unset the state
        if self.active.is_end:
            self.active.is_end = False
            self.end_marked = False
            self.apply_masks()
            return

        # Unset state for all other nodes (only one end node)
        for node in self.nodes:
            node.is_end = False

        # If current node is already start, unset the state
        if self.active.is_start:
            self.start_marked = False

        self.active.is_end = True
        self.active.is_start = False
        self.end_marked = True

        self.apply_masks()

    def delete_item(self) -> None:
        """
        Delete currently selected object, or last placed node if no object selected.

        :return: None
        """

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

    def set_active(self, new: Node | Weight | None) -> None:
        """
        Sets the active object and handles necessary changes involved in the process.

        :param new: Object to set as active
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

        # Detect clicks on text input
        if self.text_input.state and not self.text_input.clicked(event.pos):
            self.text_input.state = False
            return False

        if self.text_input.clicked(event.pos):
            self.text_input.state = True
            return False

        # Test all graph buttons
        for button in self.graph_buttons:
            if button.clicked(event.pos):
                button.callback()
                return False

        # Test all algo buttons
        for button in self.algo_buttons:
            if button.clicked(event.pos) and self.start_marked and self.end_marked:

                # Get solution from solver
                resp = button.callback()

                # If no solution has been found
                if not resp:
                    return False

                # Create timeline and give control
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

                # New name has been entered for node
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

                        # Prevent creation of overlapping weights
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

                # Convert from real to virtual coordinates
                if hasattr(event, "pos"):
                    event.pos = self.ui.get_virtual_cords(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.set_weight(event)

            self.ui.draw()
