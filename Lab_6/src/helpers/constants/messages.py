GUEST_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign in': '--> sign in to to your account',
    'sign up': '--> create new account',
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

COMMANDS_LIST_TITLE: str = '\n***** Commands (NOT case sensitive) *****\n\n'


def get_commands(list_type: str):
    global COMMANDS_LIST_TITLE
    commands_list = COMMANDS_LIST_TITLE
    commands: dict[str, str]

    if list_type == 'GUEST_COMMANDS':
        commands = GUEST_COMMANDS
    elif list_type == 'STUDENT_COMMANDS':
        commands = STUDENT_COMMANDS

    for comm in commands.keys():
        commands_list += f'{comm} {commands[comm]}\n'

    return commands_list


ROLES: dict[int, str] = {
    1: 'Guest',
    2: 'Student',
    3: 'Staff',
    4: 'Superuser'
}

