import socket
import threading
import json
import sqlite3


class Server:
    def __init__(self):
        self.napraviBazu()

    def napraviBazu(self):
        self.conn = sqlite3.connect('example.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, value TEXT)''')
        self.cursor.execute('SELECT COUNT(*) FROM data')
        count = self.cursor.fetchone()[0]
        if count > 0:
            self.cursor.execute('DELETE FROM data')
        self.conn.commit()
        with open('podaci.txt', 'w') as f:
            f.write('')

    def dodajUBazu(self, conn, addr):
        thread_conn = sqlite3.connect('example.db')
        thread_cursor = thread_conn.cursor()

        data = conn.recv(1024)
        if data:
            message = json.loads(data.decode('utf-8'))
            thread_cursor.execute("INSERT INTO data (value) VALUES (?)", (json.dumps(message),))
            thread_conn.commit()

        thread_cursor.close()
        thread_conn.close()
        conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 12345))
            s.listen()
            print('Server ceka podatke')
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=self.dodajUBazu, args=(conn, addr))
                client_thread.start()


if __name__ == "__main__":
    server = Server()
    server.start()
