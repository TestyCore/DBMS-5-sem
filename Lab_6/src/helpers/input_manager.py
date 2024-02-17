from src.helpers.constants.messages import get_commands


class Input:
    @classmethod
    def command_parse(cls, prompt: str, role: str) -> str:
        """Returns command extracted from prompt"""

        comm = prompt

        commands = get_commands(role)

        if comm not in commands.keys():  # Check if such command exists
            return f"Unknown command '{comm}'"
        else:
            return comm

    @classmethod
    def arg_parse(cls, prompt: str, isgrep: bool = False) -> tuple[str]:
        """Returns args extracted from prompt"""

        comm_args = prompt.split(maxsplit=1)

        if len(comm_args) < 2:  # If now arguments provided
            return tuple()

        comm = comm_args[0]  # Get command


        # if comm not in ALL_COMMANDS.keys():  # Check if such command exists
        #     print(f"Unknown command '{comm}'")
        #     return tuple()

        if isgrep:
            return tuple(comm_args[1])

        args_list = comm_args[1].split(',')  # Get list of arguments

        for arg in range(len(args_list)):  # Remove spaces around each argument
            args_list[arg] = args_list[arg].strip()

        args_list[:] = (value for value in args_list if value != "")

        return tuple(args_list)

    @classmethod
    def get_choice(cls, prompt: str) -> bool:
        """Returns 'y'(yes) or 'n'(no)"""

        while True:
            choice = input(prompt).lower()

            if choice == 'y':
                return True
            elif choice == 'n':
                return False

    @staticmethod
    def get_valid_username(prompt: str):
        while True:
            username = input(prompt)
            if username.isalnum() and all(char.isascii() for char in username):
                return username
            else:
                print("Invalid username. Please use only Latin characters.")

    @staticmethod
    def get_valid_password():
        while True:
            password = input("Password: ")
            if len(password.split()) == 1:
                return password
            else:
                print("Invalid password. Please use a single word without spaces.")

    @staticmethod
    def get_value_in_range(prompt, min_value, max_value):
        while True:
            try:
                user_input = int(input(prompt))
                if min_value <= user_input <= max_value:
                    return user_input
                else:
                    print(f"Please enter a value between {min_value} and {max_value}.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")


    # @classmethod
    # def get_username(cls) -> str:
    #     """Returns valid username"""
    #
    #     while True:
    #         name = input("Login as (username): ")
    #
    #         return name
