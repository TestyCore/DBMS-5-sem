from __future__ import annotations


class User:

    def __init__(self, username: str, role: str):
        self.__username = username
        self.__role = role

    @property
    def username(self) -> str:
        """Getter"""

        return self.__username

    @username.setter
    def username(self, new_username: str):
        """Setter"""

        self.__username = new_username

    @property
    def role(self):
        """Getter"""

        return self.__role

    @role.setter
    def role(self, new_role: str):
        """Setter"""

        self.__role = new_role
