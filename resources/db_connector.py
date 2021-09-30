import psycopg2

DATABASE_URL = ''

connection = psycopg2.connect(DATABASE_URL, sslmode="require")
print("connection created")


def get_connection():
    return connection
