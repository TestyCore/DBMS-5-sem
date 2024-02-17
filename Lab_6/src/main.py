from src.commands import commands
from src.db_connection import connect_db, user
from src.entities.terminal import Terminal


if __name__ == '__main__':
    term = Terminal()
    term.start()
