from src.CLI.input_handler.input_handler import InputHandler


class Console:
    def __init__(self, inputHandler: InputHandler):
        self.inputHandler = inputHandler


    def run(self):
        while True:
            user_input = self.inputHandler.handle_user_input("Enter command: ")
            print(user_input)