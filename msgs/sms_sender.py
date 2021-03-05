import messagebird
import sqlite3
import os


def fetch_contacts(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT c.phone FROM contacts as c WHERE c.phone LIKE '57%' AND  c.city LIKE 'Bogota' AND c.sent IS FALSE LIMIT 10")
    # results = [phone.split('57')[-1] for (phone,) in cursor.fetchall()]
    results = [phone for (phone,) in cursor.fetchall()]
    cursor.close()
    return results


def send_sms(conn, client, phone):
    try:
        client.message_create(
            'MessageBird',
            '+' + phone,
            os.getenv('MESSAGE_BODY')
        )

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contacts SET sent = TRUE WHERE phone like ?", (phone,))
        conn.commit()
        print('sms sent')
    except messagebird.client.ErrorException as e:
        print(e)
        print('Error sending the sms')


if __name__ == '__main__':
    conn = sqlite3.connect('contacts.db', timeout=10)
    contacts = fetch_contacts(conn)
    key = os.getenv('MESSAGEBIRD_ACCESS_KEY')
    client = messagebird.Client(key)
    for contact in contacts:
        print(contact)
        send_sms(conn, client, contact)
