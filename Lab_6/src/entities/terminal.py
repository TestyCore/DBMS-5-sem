from __future__ import annotations

from src.entities.database import Database
from src.entities.user import User
from src.helpers.constants.messages import get_commands, ROLES
from src.helpers.input_manager import Input


class Terminal:

    def __init__(self):
        self.__prompt: str | None = None
        self.__user: User | None = None
        self.__db: Database | None = None

    def start(self):
        """Entry point of CLI"""

        self.__user = User('Guest', ROLES[1])
        self.__db = Database()

        self.list_command()

        while True:
            self.__prompt = input(f'{self.__user.username}: ').lower()
            comm = Input.command_parse(self.__prompt)

            if comm == 'list':
                self.list_command()
            elif comm == 'sign in':
                self.sign_in_command()
            elif comm == 'sign up':
                pass
            elif comm == 'articles':
                pass
            elif comm == 'reviews':
                pass
            elif comm == 'school info':
                pass
            elif comm == 'exit':
                pass
            elif comm == 'switch':
                pass
            elif comm == 'exit':
                pass
            else:
                print(comm)

    def list_command(self):

        if self.__user.role == ROLES[1]:
            # Guest
            print(get_commands('GUEST_COMMANDS'))
        elif self.__user.role == ROLES[2]:
            print(get_commands('STUDENT_COMMANDS'))

    def sign_in_command(self):
        username = input("\nUsername: ").strip()
        password = input("Password: ").strip()

        result = self.__db.sign_in(username, password)

        if result.__len__() == 0:
            print('\nUsername or password is not valid\n')
            return

        self.__user.username = result[0]

        is_staff = result[1]
        is_superuser = result[2]

        if is_staff is False and is_superuser is False:
            self.__user.role = ROLES[2]
        elif is_staff is True and is_superuser is False:
            self.__user.role = ROLES[3]
        elif is_staff is False and is_superuser is True:
            self.__user.role = ROLES[4]



