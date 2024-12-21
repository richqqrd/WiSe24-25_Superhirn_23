class InputHandler:

    def handle_user_input(self, prefix: str):
        user_input = input(prefix)
        return user_input

    def handle_menu_input(self) -> str:
        """
        Handles input for the main menu (1-6).
        """
        return self.handle_user_input("Enter command: ")

    def handle_role_input(self) -> str:
        """
        Handles input for role selection (1-2).
        """
        return self.handle_user_input("Enter role: ")

    def handle_language_input(self) -> str:
        """
        Handles input for language selection (1-2).
        """
        return self.handle_user_input("Enter language: ")

    def handle_code_input(self) -> str:
        """
        Handles input for code generation.
        """
        return self.handle_user_input("Enter input for secret code (5 digits): ")

    def handle_guess_input(self) -> str:
        """
        Handles input for code guessing.
        """
        return self.handle_user_input("Enter your guess (5 digits): ")

    def handle_feedback_input(self) -> str:
        """
        Handles input for feedback generation.
        """
        return self.handle_user_input("Enter feedback (5 digits): ")
