from datetime import datetime

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

        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s;"

            self.__cursor.execute(query, (username, password))

            response = self.__cursor.fetchone()

            if response:
                return response[0], response[3], response[6], response[7]
            else:
                return tuple()

        except Exception as e:
            return None

    def sign_up(self, first_name: str,  last_name: str, username: str, password: str,
                email: str, is_staff: bool, is_superuser: bool) -> bool:
        try:
            query = "insert into users (first_name, last_name, username, password, email," \
                    " is_staff, is_superuser) values (%s, %s, %s, %s, %s, %s, %s);"

            self.__cursor.execute(query, (first_name, last_name, username, password, email, is_staff, is_superuser))
            self.__connection.commit()

            return True

        except Exception as e:
            return False

    def table_len(self, table_name: str) -> int:
        try:
            query = f"SELECT COUNT(*) FROM {table_name};"
            self.__cursor.execute(query)
            row_count = self.__cursor.fetchone()[0]

            return row_count

        except Exception as e:
            return None

    def get_data(self, table_name: str, amount: int, order_by: str) -> list:
        try:
            query = f"SELECT * FROM {table_name} ORDER BY {order_by} DESC LIMIT {amount};"
            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            return None

    def get_staff(self, amount: int) -> list:
        try:
            query = "SELECT users.first_name || ' ' || users.last_name AS Teacher, " \
                    "subject.name AS Nauka " \
                    "FROM teacher " \
                    "INNER JOIN users ON users.id = teacher.users_id " \
                    f"INNER JOIN subject ON subject.id = teacher.subject_id LIMIT {amount};"

            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            print(e)
            return None

    def get_schedule(self, user_id: str):
        try:
            query = "SELECT " \
                        "class.name AS class, " \
                        "subject.name AS subject, " \
                        "cabinet.name AS cabinet, " \
                        "lesson_time.time_start, " \
                        "lesson_time.time_end, " \
                        "timetable.day_of_week " \
                    "FROM timetable " \
                    "INNER JOIN class ON class.id = timetable.class_id " \
                    "INNER JOIN subject ON subject.id = timetable.subject_id " \
                    "INNER JOIN cabinet ON cabinet.id = timetable.cabinet_id " \
                    "INNER JOIN lesson_time ON lesson_time.id = timetable.lesson_time_id " \
                    "INNER JOIN student ON student.class_id = timetable.class_id " \
                    f"WHERE student.users_id = {user_id};"

            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            return None

    def get_grades(self, user_id: str):
        try:
            query = "SELECT " \
                    "users.id AS User_id, " \
                    "subject.name AS Subject, " \
                    "grade_journal.grade AS Grade, " \
                    "grade_journal.date AS Date " \
                    "FROM users " \
                    "INNER JOIN student ON users.id = student.users_id " \
                    "INNER JOIN grade_journal ON student.id = grade_journal.student_id " \
                    f"INNER JOIN subject ON grade_journal.subject_id = subject.id WHERE users.id = {user_id}; "

            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return  response

        except Exception as e:
            pass

    def get_speciality(self, user_id: str) -> str:
        try:
            query = "SELECT " \
                        "subject.name AS Subject " \
                    "FROM users " \
                    "INNER JOIN teacher ON users.id = teacher.users_id " \
                    "INNER JOIN subject ON teacher.subject_id = subject.id " \
                    f"WHERE users.id = {user_id};"

            self.__cursor.execute(query)
            response = self.__cursor.fetchone()[0]

            return  response

        except Exception as e:
            return None

    def get_table_ids(self, table_name: str):
        try:
            query = "SELECT " \
                    "id " \
                    f"FROM {table_name};"

            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            return None

    def set_grade(self, student_id: int, subject: str, grade: int, date: str) -> bool:
        try:
            query = "SELECT " \
                    "id " \
                    "FROM subject " \
                    f"WHERE name = '{subject}';"

            self.__cursor.execute(query)
            subject_id = self.__cursor.fetchone()[0]

            query = "insert into grade_journal (grade, student_id, subject_id, date) " \
                    "values (%s, %s, %s, %s);"

            self.__cursor.execute(query, (grade, student_id, subject_id, date))
            self.__connection.commit()

            return True

        except Exception as e:
            return False

    def publish_article(self, title: str, author_id: int, date: str, content: str) -> bool:
        try:
            query = "insert into article (title, author_id, date, content) " \
                    "values (%s, %s, %s, %s);"

            self.__cursor.execute(query, (title, author_id, date, content))
            self.__connection.commit()

            return True

        except Exception as e:
            return False

    def update_user_info(self, user_id: int, first_name: str, last_name: str, username: str, password: str, email: str,) -> bool:
        try:
            query = f"UPDATE users SET first_name = %s, last_name = %s, username = %s, password = %s, email = %s where id = {user_id};"

            self.__cursor.execute(query, (first_name, last_name, username, password, email))
            self.__connection.commit()

            return True

        except Exception as e:
            return False

    def get_all_classes(self):
        try:
            query = f"SELECT name FROM class;"
            self.__cursor.execute(query)
            classes_list = self.__cursor.fetchall()

            return classes_list

        except Exception as e:
            return None

    def get_class_id(self, class_name: str):
        class_name = class_name[:1] + "'" + class_name[1:]
        class_name = class_name[:4] + "'" + class_name[4:]
        try:
            query = f"SELECT id FROM class WHERE name = '{class_name}';"
            self.__cursor.execute(query)
            classes_list = self.__cursor.fetchall()

            return classes_list

        except Exception as e:
            return None

    def get_lessons_list(self, class_id: int, day: str):
        try:
            query = "SELECT " \
                        "id " \
                    "FROM timetable " \
                    f"WHERE class_id = {class_id}  AND day_of_week = '{day}';"
            self.__cursor.execute(query)
            id_list = self.__cursor.fetchall()

            return id_list

        except Exception as e:
            return None

    def update_timetable(self, lesson_id: int, subject_id: int, cabinet_id: int, lesson_time_id: int):
        try:
            query = f"UPDATE timetable SET subject_id = %s, cabinet_id = %s, lesson_time_id = %s where id = {lesson_id};"

            self.__cursor.execute(query, (subject_id, cabinet_id, lesson_time_id))
            self.__connection.commit()

            return True

        except Exception as e:
            return False

    def get_logs(self, user_id: int):
        try:
            query = "SELECT " \
                        "journal.users_id, journal.date, action_type.name " \
                    "FROM journal " \
                    "INNER JOIN action_type ON journal.action_type_id = action_type.id " \
                    f"WHERE journal.users_id = {user_id};"
            self.__cursor.execute(query)
            id_list = self.__cursor.fetchall()

            return id_list

        except Exception as e:
            return None






