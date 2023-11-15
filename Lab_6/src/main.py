from src.commands import commands
from src.db_connection import connect_db, user
from src.entities.terminal import Terminal


# def start_app():
#     connect_db()
#     commands.get('list')()
#
#     while True:
#         user_input = input(user).strip()
#
#         selected_command = commands.get(user_input.lower(), None)
#
#         if selected_command:
#             selected_command()
#         else:
#             print("Invalid command. Please try again.")


if __name__ == '__main__':
    term = Terminal()
    term.start()
