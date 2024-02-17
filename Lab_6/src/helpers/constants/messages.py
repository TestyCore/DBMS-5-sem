GUEST_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign in': '--> sign in to to your account',
    'articles': '--> list of all articles',
    'reviews': '--> list of all reviews',
    'staff': '--> list of all teachers',
    'school info': '--> info about the school',
    'exit': '--> quit the app'
}


STUDENT_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign out': '--> sign out of your account',
    'articles': '--> list of all articles',
    'reviews': '--> list of all reviews',
    'staff': '--> list of all teachers',
    'school info': '--> info about the school',
    'schedule': '--> view personal timetable',
    'grades': '--> view personal grades',
    'exit': '--> quit the app'
}

STAFF_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign out': '--> sign out of your account',
    'articles': '--> list of all articles',
    'reviews': '--> list of all reviews',
    'staff': '--> list of all teachers',
    'school info': '--> info about the school',
    'rate': '--> give grade to student',
    'exit': '--> quit the app'
}

SUPERUSER_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign out': '--> sign out of your account',
    'sign up': '--> create new account',
    'create article': '--> create new articles',
    'edit user': "--> edit user's personal info",
    'edit schedule': '--> edit schedule',
    'view logs': "--> view user's logs",
    'exit': '--> quit the app'
}

COMMANDS_LIST_TITLE: str = '\n***** Commands (NOT case sensitive) *****\n\n'


def get_commands_list(list_type: str) -> str:
    global COMMANDS_LIST_TITLE
    commands_list = COMMANDS_LIST_TITLE
    commands: dict[str, str]

    if list_type == 'GUEST_COMMANDS':
        commands = GUEST_COMMANDS
    elif list_type == 'STUDENT_COMMANDS':
        commands = STUDENT_COMMANDS
    elif list_type == 'STAFF_COMMANDS':
        commands = STAFF_COMMANDS
    elif list_type == 'SUPERUSER_COMMANDS':
        commands = SUPERUSER_COMMANDS

    for comm in commands.keys():
        commands_list += f'{comm} {commands[comm]}\n'

    return commands_list


def get_commands(dict_type: str) -> dict:
    if dict_type == 'Guest':
        return GUEST_COMMANDS
    elif dict_type == 'Student':
        return STUDENT_COMMANDS
    elif dict_type == 'Staff':
        return STAFF_COMMANDS
    elif dict_type == 'Superuser':
        return SUPERUSER_COMMANDS


ROLES: dict[int, str] = {
    1: 'Guest',
    2: 'Student',
    3: 'Staff',
    4: 'Superuser'
}

