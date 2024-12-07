from CLI.console import Console
from CLI.input_handler.input_handler import InputHandler


def main():
    ui = Console(InputHandler())
    ui.run()


if __name__ == "__main__":
    main()