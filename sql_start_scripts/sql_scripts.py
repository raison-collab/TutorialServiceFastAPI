import psycopg2

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

roles = [
    "Ученик",
    "Учитель"
]

subjects = [
    "Математика",
    "Физика",
    "Химия",
    "Биология",
    "История",
    "Литература",
    "Иностранные языки",
    "Информатика",
    "География",
    "Экономика",
    "Право",
    "Философия",
    "Психология",
    "Социология",
    "Искусство",
    "Музыка"
]

connection = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

cursor = connection.cursor()


def save_data():
    for index, el in enumerate(roles, start=1):
        try:
            cursor.execute(f"INSERT INTO role(id, name) VALUES({index}, '{el}')")
        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            continue

    print("[DB] Внесены данные о ролях")

    for index, el in enumerate(subjects, start=1):
        try:
            cursor.execute(f"INSERT INTO subject(id, name) VALUES({index}, '{el}')")
        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            continue

    print("[DB] внесены данные о предметах")

    connection.commit()
    connection.close()
