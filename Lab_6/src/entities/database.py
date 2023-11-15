import psycopg2


class Database:

    def __init__(self):
        self.__connection = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='school',
            user='brr',
            password='qwerty'
        )
        self.__cursor = self.__connection.cursor()

    def sign_in(self, username: str, password: str) -> tuple:
        """
        :return: tuple of strings: username, is_staff, is_superuser
        """
        query = "SELECT * FROM users WHERE username = %s AND password = %s;"

        self.__cursor.execute(query, (username, password))

        results = self.__cursor.fetchone()

        if results:
            return results[3], results[6], results[7]
        else:
            return tuple()

