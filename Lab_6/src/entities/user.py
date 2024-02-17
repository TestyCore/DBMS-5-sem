from __future__ import annotations


class User:

    def __init__(self, user_id: str, username: str, role: str):
        self.__id = user_id
        self.__username = username
        self.__role = role

    @property
    def id(self) -> str:
        """Getter"""

        return self.__id

    @id.setter
    def id(self, new_id: str):
        """Setter"""

        self.__id = new_id

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
