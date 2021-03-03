import csv
import sqlite3


def process(conn):
    with open('out.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            phone = row[2]
            city = row[1]
            category = row[0]
            print(f'Inserting {phone}')
            insert_record(conn, (phone, city, category, False))
            line_count += 1
        print(f'Processed {line_count} lines')


def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE contacts(phone text PRIMARY KEY, city text, category text, sent boolean)')
        conn.commit()
        print('DB created')
    except sqlite3.OperationalError as e:
        print('DB already created')


def insert_record(conn, entities):
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO contacts(phone, city, category, sent) VALUES(?, ?, ?, ?)', entities)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print('Record already inserted')


if __name__ == '__main__':
    conn = sqlite3.connect('contacts.db')
    create_table(conn)
    process(conn)
