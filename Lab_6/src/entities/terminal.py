from __future__ import annotations
from datetime import datetime

import sys

from src.entities.database import Database
from src.entities.user import User
from src.helpers.constants.messages import get_commands_list, ROLES
from src.helpers.input_manager import Input


class Terminal:

    def __init__(self):
        self.__prompt: str | None = None
        self.__user: User | None = None
        self.__db: Database | None = None

    def start(self):
        """Entry point of CLI"""

        self.__user = User(str(0), 'Guest', ROLES[1])
        self.__db = Database()

        self.list_command()

        while True:
            self.__prompt = input(f'{self.__user.username}: ').lower()
            comm = Input.command_parse(self.__prompt, self.__user.role)

            if comm == 'list':
                self.list_command()
            elif comm == 'sign in':
                self.sign_in_command()
            elif comm == 'sign up':
                self.sign_up_command()
            elif comm == 'sign out':
                self.sign_out_command()
            elif comm == 'articles':
                self.articles_command()
            elif comm == 'reviews':
                self.reviews_command()
            elif comm == 'staff':
                self.staff_command()
            elif comm == 'school info':
                self.school_info_command()
            elif comm == 'schedule':
                self.schedule_command()
            elif comm == 'grades':
                self.grades_command()
            elif comm == 'rate':
                self.rate_command()
            elif comm == 'create article':
                self.create_article_command()
            elif comm == 'edit user':
                self.edit_user_command()
            elif comm == 'edit schedule':
                self.edit_schedule_command()
            elif comm == 'view logs':
                self.view_logs_command()
            elif comm == 'exit':
                sys.exit()
            else:
                print(comm)

    def list_command(self):

        if self.__user.role == ROLES[1]:
            print(get_commands_list('GUEST_COMMANDS'))
        elif self.__user.role == ROLES[2]:
            print(get_commands_list('STUDENT_COMMANDS'))
        elif self.__user.role == ROLES[3]:
            print(get_commands_list('STAFF_COMMANDS'))
        elif self.__user.role == ROLES[4]:
            print(get_commands_list('SUPERUSER_COMMANDS'))

    def sign_in_command(self):
        username = Input.get_valid_username('Username: ')
        password = Input.get_valid_password()

        response = self.__db.sign_in(username, password)

        if response is None:
            print('\nError signing in\n')

        if response.__len__() == 0:
            print('\nUsername or password is not valid\n')
            return

        self.__user.id = response[0]
        self.__user.username = response[1]

        is_staff = response[2]
        is_superuser = response[3]

        self.assign_role(is_staff, is_superuser)

    def sign_out_command(self):
        self.__user.username = 'Guest'
        self.__user.role = ROLES[1]

    def sign_up_command(self):
        first_name = Input.get_valid_username('First_name: ')
        last_name = Input.get_valid_username('Last_name: ')
        username = Input.get_valid_username('Username: ')
        password = Input.get_valid_password()
        email = Input.get_valid_username('Email: ')

        while True:
            is_staff = Input.get_choice('is_staff ? [y/n]: ')
            is_superuser = Input.get_choice('is_superuser ? [y/n]: ')

            if is_staff is True and is_superuser is True:
                print("ERROR: 'is_staff' and 'is_superuser can not be both true'")
            else:
                break

        response = self.__db.sign_up(first_name, last_name, username, password, email, is_staff, is_superuser)

        if response:
            print("User successfully signed up.")
            self.__user.username = username
            self.assign_role(is_staff, is_superuser)
        else:
            print(f"Error signing up user")

    def assign_role(self, is_staff: bool, is_superuser: bool):
        if is_staff is False and is_superuser is False:
            self.__user.role = ROLES[2]
        elif is_staff is True and is_superuser is False:
            self.__user.role = ROLES[3]
        elif is_staff is False and is_superuser is True:
            self.__user.role = ROLES[4]

    def articles_command(self):
        amount = self.get_table_len('article')
        articles = self.__db.get_data('article', amount, 'date')

        print('\n\n')
        for index, article in enumerate(articles, start=1):
            print(f'   ********** Article #{index} **********')
            print(f'Title: {article[1]}')
            print(f'Date: {article[3]}')
            print(f'Content: {article[4]}\n\n')

    def reviews_command(self):
        amount = self.get_table_len('review')
        reviews = self.__db.get_data('review', amount, 'date')

        avg_rate = 0

        print('\n\n')
        for index, review in enumerate(reviews, start=1):
            print(f'   ********** Review #{index} **********')
            print(f'Date: {review[2]}')
            print(f'Content: {review[3]}')
            print(f'Rate: {review[4]}\n\n')

            avg_rate += int(review[4])

        avg_rate /= reviews.__len__()

        print(f'Average rate: {avg_rate}\n\n')

    def get_table_len(self, table_name: str):
        response = self.__db.table_len(table_name)

        if response is None:
            print(f"Error getting table length")
            return

        print(f'\nFound {response} records.')

        return Input.get_value_in_range('How many to display? ', 1, response)

    def school_info_command(self):
        print('\nName: BSUIR')
        print('Address: Hikalo, 9')
        print('Phone: +375-29-777-77-77\n')

    def staff_command(self):
        amount = self.get_table_len('teacher')
        staff = self.__db.get_staff(amount)

        print('\n\n')
        for index, teacher in enumerate(staff, start=1):
            print(f' Teacher #{index}')
            print(f'Name: {teacher[0]}')
            print(f'Subject: {teacher[1]}\n\n')

    def schedule_command(self):
        schedule = self.__db.get_schedule(self.__user.id)

        if schedule is None:
            print('\nError retrieving schedule')

        print(f'\n\n***** Schedule for {self.__user.username} ({schedule[0][0]}) *****\n')
        print(f'{schedule[0][5]}:')

        current_day = None
        index = 1
        for day in schedule:
            if current_day is not None and current_day != day[5]:
                print(f"\n\n{day[5]}")
                index = 1

            print(f'\nLesson #{index}')
            print(f'Subject: {day[1]}')
            print(f'Classroom: {day[2]}')
            print(f'Lesson time: {day[3]} - {day[4]}')

            index += 1
            current_day = day[5]

        print('\n\n')

    def grades_command(self):
        grades = self.__db.get_grades(self.__user.id)

        if grades is None:
            print('\nError retrieving grades')
            return

        if not grades:
            print('\nNo grades')
            return

        print(f"\n\n***** {self.__user.username}'s grades  *****\n")
        print(f'{grades[0][3]}:')

        current_day = None
        index = 1
        for grade in grades:
            if current_day is not None and current_day != grade[3]:
                print(f"\n\n{grade[3]}")
                index = 1

            print(f'\nGrade #{index}')
            print(f'Subject: {grade[1]}')
            print(f'Value: {grade[2]}')

            index += 1
            current_day = grade[3]

        print('\n\n')

    def rate_command(self):
        subject = self.__db.get_speciality(self.__user.id)

        print(f'\n(You are major in {subject})\n')

        students_id_list = self.__db.get_table_ids('student')
        students_id_list = [element for tup in students_id_list for element in tup]

        while True:
            student_id = Input.get_value_in_range("Student id: ", 1, max(students_id_list))

            if student_id not in students_id_list:
                print('Invalid id, student not found')
            else:
                break

        current_date = datetime.now().strftime('%Y-%m-%d')
        grade = Input.get_value_in_range("Grade: ", 1, 10)

        if self.__db.set_grade(student_id, subject, grade, current_date):
            print('The grade has been successfully set')
        else:
            print('Error occurred setting the grade')

    def create_article_command(self):
        users_id_list = self.__db.get_table_ids('users')
        users_id_list = [element for tup in users_id_list for element in tup]

        while True:
            author_id = Input.get_value_in_range("Author id: ", 1, max(users_id_list))

            if author_id not in users_id_list:
                print('Invalid id, user not found')
            else:
                break

        title = input('Title: ')
        current_date = datetime.now().strftime('%Y-%m-%d')
        content = input('Content: ')

        if self.__db.publish_article(title, author_id, current_date, content):
            print('The article has been successfully published')
        else:
            print('Error occurred publishing the article')

    def edit_user_command(self):
        users_id_list = self.__db.get_table_ids('users')
        users_id_list = [element for tup in users_id_list for element in tup]

        while True:
            user_id = Input.get_value_in_range("id of user to edit: ", 1, max(users_id_list))

            if user_id not in users_id_list:
                print('Invalid id, user not found')
            else:
                break

        first_name = Input.get_valid_username('First_name: ')
        last_name = Input.get_valid_username('Last_name: ')
        username = Input.get_valid_username('Username: ')
        password = Input.get_valid_password()
        email = Input.get_valid_username('Email: ')

        if self.__db.update_user_info(user_id, first_name, last_name, username, password, email):
            print('The user has been successfully updated')
        else:
            print('Error occurred updating user')

    def edit_schedule_command(self):
        classes = self.__db.get_all_classes()
        classes = [element for tup in classes for element in tup]
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        while True:
            class_prompt = input("Class: ")

            if class_prompt not in classes:
                print("Invalid class, valid example: 9'A'")
            else:
                break

        while True:
            day = Input.get_valid_username("Day of week: ")

            if day not in days_of_week:
                print("Invalid day, valid example: 'Monday'")
            else:
                break

        class_id = self.__db.get_class_id(class_prompt)
        class_id = [element for tup in class_id for element in tup]

        lessons_id = self.__db.get_lessons_list(class_id[0], day)
        lessons_id = [element for tup in lessons_id for element in tup]

        lesson = Input.get_value_in_range(f'Pick 1 of {lessons_id.__len__()} lessons to edit: ', 1, lessons_id.__len__())

        subject = Input.get_value_in_range("Lesson: ", 1, 13)
        classroom = Input.get_value_in_range("Classroom: ", 1, 48)
        lesson_time = Input.get_value_in_range("Lesson time: ", 1, 8)

        if self.__db.update_timetable(lessons_id[lesson - 1], subject, classroom, lesson_time):
            print('The timetable has been successfully updated')
        else:
            print('Error occurred updating timetable')

    def view_logs_command(self):
        users_id_list = self.__db.get_table_ids('users')
        users_id_list = [element for tup in users_id_list for element in tup]

        while True:
            user_id = Input.get_value_in_range("user id for viewing logs: ", 1, max(users_id_list))

            if user_id not in users_id_list:
                print('Invalid id, user not found')
            else:
                break

        logs = self.__db.get_logs(user_id)

        if logs is None:
            print('\nError retrieving logs')

        if not logs:
            print(f'No logs were registered for user_id {user_id}')
            return

        print(f'\n\n***** Logs for {self.__user.username} *****\n')

        current_day = None
        index = 1
        for index, log in enumerate(logs, start=1):

            print(f'\nLog #{index}')
            print(f'Date: {log[1]}')
            print(f'Action: {log[2]}\n')

        print('\n\n')



















