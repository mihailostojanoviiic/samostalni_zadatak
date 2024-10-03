import socket
import json
from datetime import datetime
import tkinter as tk
from functools import reduce
from tkinter import messagebox, Toplevel, Text
import sqlite3


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacija")
        self.root.configure(bg='#f0f0f0')

        self.gui()

    def gui(self):
        tk.Label(self.root, text="Ime:", bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Godine:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Pošalji", command=self.posalji, bg='#4caf50', fg='white').grid(row=2, columnspan=2, padx=10, pady=10)

        tk.Button(self.root, text="Prikaži poslednji upis", command=self.prikaziPoslednji, bg='#2196f3', fg='white').grid(row=3,columnspan=2,padx=10, pady=10)
    def upis(self):
        lista = [1, 2, 3, 4, 5]         #lista
        ime = self.name_entry.get()
        godine = self.age_entry.get()

        if not godine.isdigit():
            messagebox.showerror("Greška", "Godine moraju biti broj.")
            return None

        recnik = {'ime': ime, 'godine': int(godine)}        #recnik
        ntorka = (10, 20, 30)           #ntorka
        funkcija = lambda x: x * 2          #lambda

        mapiran = list(map(funkcija, lista))            #map funkcija
        filtriran = list(filter(lambda x: x > 2, lista))        #filter
        redukovan = reduce(lambda x,y:x+y,lista)      #redukcija

        data = {
            'lista': lista,
            'recnik': recnik,
            'ntorka': ntorka,
            'map': mapiran,
            'filter': filtriran,
            'redukcija': redukovan,
            'datum': datetime.now().strftime("%d-%m-%Y"),       #datum
            'vreme': datetime.now().strftime("%H:%M:%S")        #vreme
        }
        return data

    def posalji(self):
        data = self.upis()
        if data is None:
            return

        with open('podaci.txt','a') as f:           #rad sa datotekom
            f.write(json.dumps(data)+'\n')

        message = json.dumps(data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12345))
            s.sendall(message.encode('utf-8'))

        messagebox.showinfo("Odgovor servera", "Uspesno upisano u bazu podataka")

    def formatiraj(self, data):
        ispis = ""
        ispis += "lista: " + ",".join(map(str, data['lista'])) + "\n"
        ispis += "recnik: " + "; ".join(f"{i}:{j}" for i, j in data['recnik'].items()) + "\n"
        ispis += "ntorka: " + ",".join(map(str, data['ntorka'])) + "\n"
        ispis += "map: " + ",".join(map(str, data['map'])) + "\n"
        ispis += "filter: " + ",".join(map(str, data['filter'])) + "\n"
        ispis += "redukcija: " + str(data['redukcija']) + "\n"
        ispis += "datum: " + data['datum'] + "\n"
        ispis += "vreme: " + data['vreme'] + "\n"
        return ispis
    def prikaziPoslednji(self):
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            poslednji_upis = json.loads(row[0])
            upis_str = self.formatiraj(poslednji_upis)

            top = Toplevel(self.root)
            top.title("Poslednji upis")
            text = Text(top)
            text.insert(tk.END, upis_str)
            text.pack()

        else:
            messagebox.showinfo("Poslednji upis", "Nema unosa u bazi podataka")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
