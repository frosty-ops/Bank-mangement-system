import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="bank_management",
        user="postgres",
        password="KIRTI",
        port="5432"
    )