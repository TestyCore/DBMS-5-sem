from src.helpers.constants.messages import GUEST_COMMANDS


class Input:
    @classmethod
    def command_parse(cls, prompt: str) -> str:
        """Returns command extracted from prompt"""

        comm = prompt

        if comm not in GUEST_COMMANDS.keys():  # Check if such command exists
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

        if comm not in GUEST_COMMANDS.keys():  # Check if such command exists
            print(f"Unknown command '{comm}'")
            return tuple()

        if isgrep:
            return tuple(comm_args[1])

        args_list = comm_args[1].split(',')  # Get list of arguments

        for arg in range(len(args_list)):  # Remove spaces around each argument
            args_list[arg] = args_list[arg].strip()

        args_list[:] = (value for value in args_list if value != "")

        return tuple(args_list)

    @classmethod
    def get_choice(cls, prompt: str) -> str:
        """Returns 'y'(yes) or 'n'(no)"""

        while True:
            choice = input(prompt)

            if choice == 'y' or choice == 'n':
                return choice

    @classmethod
    def validate_username(cls, name: str) -> bool:
        """Checks if name consists only from latin letters"""

        name = name.strip()

        # if match is not None and name == match.group(0):
        #     return True
        # else:
        #     return False

    @classmethod
    def get_username(cls) -> str:
        """Returns valid username"""

        while True:
            name = input("Login as (username): ")

            return name
