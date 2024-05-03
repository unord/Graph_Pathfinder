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
        self.current_pos = -1
        self.current_path = timeline[0]
        self.active_paths = []
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

# lav back og forward om hvor du bruger current_path og active_paths til at tegne

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

        for path in self.active_paths:
            for node in path.nodes:
                node.set_name(str(path.length_to_node(node)))
        
        for weight in self.weights:
            weight.set_default()
        
        for path in self.active_paths:
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
                    weight.is_searching = False
                    weight.is_searched = True

        for weight in self.current_path.weights:
            weight.is_searching = True
            weight.is_searched = False

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

        while True:
            for event in pygame.event.get():
                self.quit_func(event)
                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
            self.draw()
