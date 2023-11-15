import psycopg2

user = '> '


def connect_db():
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'school'
    DB_USER = 'brr'
    DB_PASSWORD = 'qwerty'

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = connection.cursor()

    return cursor


# def close_db():
#     cursor.close()
#     connection.close()


def db_sign_in(username, password):
    cursor = connect_db()

    query = "SELECT * FROM users WHERE username = %s AND password = %s;"

    cursor.execute(query, (username, password))

    results = cursor.fetchall()

    if results:
        user = username
    else:
        print('\nUsername or password is not valid\n')

