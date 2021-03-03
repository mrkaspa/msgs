import messagebird
import sqlite3


def fetch_contacts(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT c.phone FROM contacts as c WHERE c.city LIKE 'Bogota' AND c.sent IS FALSE")
    results = [phone for (phone,) in cursor.fetchall()]
    cursor.close()
    return results


def send_sms(conn, client, phone):
    try:
        client.message_create(
            'MessageBird',
            '31XXXXXXXXX',
            'Hi! This is your first message'
        )

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contacts SET sent = TRUE WHERE phone like ?", (phone,))
        conn.commit()
    except messagebird.client.ErrorException as e:
        print('Error sending the sms')


if __name__ == '__main__':
    conn = sqlite3.connect('contacts.db', timeout=10)
    contacts = fetch_contacts(conn)
    conn.close()
    conn = sqlite3.connect('contacts.db', timeout=10)
    client = messagebird.Client('ACCESS_KEY')
    for contact in contacts:
        print(contact)
        send_sms(conn, client, contact)
