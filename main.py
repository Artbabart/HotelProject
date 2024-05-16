#Megvalósításra vár még:
#1 Az index alapú törlés az összes 3-as szobaszámú foglalást törli
#2 A plusz szobák hozzáadásánál 3 felé megy a szobák indexe

import tkinter as tk
from tkinter import messagebox
import json
from Room import *
from Hotel import Hotel
from datetime import datetime

room1 = Room(1, "egyagyas",date="2023-12-31", price=2000)
room2 = Room(2, "ketagyas", date="2024-12-24", price=3000)
room3 = Room(3, "ketagyas", date="2024-02-28", price=3000)
room4 = Room(2, "ketagyas", date="2024-05-02", price=3000)
room5 = Room(1, "egyagyas", date="2024-11-23", price=2000)
hotel = Hotel("Teszt szalloda", [room1, room2, room3, room4, room5])

foglalasok_json = [
        (room1.serialize()),
        (room2.serialize()), 
        (room3.serialize()),
        (room4.serialize()),
        (room5.serialize()),]

with open('foglalasok.json', 'w') as f:
            json.dump(foglalasok_json, f, indent=4)

bookedrooms = []

root = tk.Tk()
root.title("Szálloda")
root.configure(background='skyblue')

hotelName = tk.Label(text="Szálloda", font=("Arial", 20), background="gold")
hotelName.pack(padx=40, pady=40)

def getBookedRooms():
    return bookedrooms

def chooseOptions(value):
    print("Kiválasztva:", value)

options = ["egyagyas", "ketagyas"]
choosed = tk.StringVar(root)
choosed.set(options[0])
optionmenu = tk.OptionMenu(root, choosed, *options, command=chooseOptions)
optionmenu.config(width=43, border=10, background="gold")

class BookingOperation:
    def __init__(self, booked_rooms):
        self.booked_rooms = booked_rooms

    def booking(self, input_room_type, date_str):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            date_today = datetime.now().date()

            if date < date_today:
                messagebox.showinfo("Hiba!", "Csak mai vagy későbbi dátum foglalható!")
                return
            
            same_date_rooms = [room for room in self.booked_rooms if room.date == date_str]

            if len(same_date_rooms) >= 3:
                messagebox.showinfo("Hiba!", f"Az adott dátumra már elfogytak a szobák: ({date_str}). Kérlek, válassz másik dátumot!")
                return

            if input_room_type.lower() == "egyagyas":
                room = Room(len(self.booked_rooms) + 1, input_room_type, date.strftime("%Y-%m-%d"), price=2000)
                self.booked_rooms.append(room)

            elif input_room_type.lower() == "ketagyas":
                room = Room(len(self.booked_rooms) + 1, input_room_type, date.strftime("%Y-%m-%d"), price=3000)
                self.booked_rooms.append(room)

            else:
                print("hiba")

            messagebox.showinfo("Sikeres foglalás!", "A foglalása sikeres volt, bekerült a rendszerbe!")

            if len(same_date_rooms) == 3:
                input.delete(0, tk.END)
                input.insert(0, mindate.strftime("%Y-%m-%d"))

            # JSON-be konvertálás
            booking_json = room.serialize()
            with open('foglalasok.json', 'r+') as f:
                data = json.load(f)
                data.append(booking_json)
                f.seek(0)
                json.dump(data, f, indent=4)
        except ValueError as e:
            print(e)

mindate = datetime.now().date()
input = tk.Entry(root, width=50, border=10, bg="gold")
input.insert(0, mindate.strftime("%Y-%m-%d"))

def listing_button_click():
    booked_room_list.delete(0, tk.END)
    try:
        with open('foglalasok.json', 'r') as f:
            booked_rooms = json.load(f)
            for booking in booked_rooms:
                booked_room_list.insert(tk.END, f"Szoba száma: {booking['id']} | Szoba típusa: {booking['type']} | Dátum: {booking['date']} | Szoba ára: {booking['ar']}")
    except FileNotFoundError:
        booked_room_list.insert(tk.END, "Nincs foglalás rögzítve.")

booked_room_list = tk.Listbox(root, width=80, height=10, background="gold")
booked_room_list.pack(padx=50, pady=10)

def delete_bookings():
    try:
        set_index = booked_room_list.curselection()
        if not set_index:
            messagebox.showinfo("Nincs kijelölve!", "Nincs kijelölt foglalás a törléshez.")
            return
        else:
            set_bookings = [booked_room_list.get(index) for index in set_index]
            for booking_text in set_bookings:
                room_number = booking_text.split("|")[0].split(":")[1].strip()
                with open('foglalasok.json', 'r+') as f:
                    bookings = json.load(f)
                    bookings = [booking for booking in bookings if booking['id'] != int(room_number)]
                    f.seek(0)
                    json.dump(bookings, f, indent=4)
                    f.truncate()
            for index in sorted(set_index, reverse=True):
                booked_room_list.delete(index)
            messagebox.showinfo("Foglalások törölve", "A kijelölt foglalások sikeresen törölve lettek.")
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba történt a foglalások törlése közben: {str(e)}")

booking_operation = BookingOperation(bookedrooms)
button1 = tk.Button(
    root,
    command=lambda: booking_operation.booking(choosed.get(), input.get()),
    text="Foglalás",
    activebackground="skyblue",
    activeforeground="white",
    anchor="center",
    bd=3,
    bg="skyblue",
    disabledforeground="grey",
    fg="black",
    font=("Arial", 12),
    height=2,
    highlightbackground="black",
    highlightcolor="green",
    highlightthickness=2,
    justify="center",
    overrelief="raised",
    padx=10,
    pady=5,
    width=15,
    wraplength=100
)

button2 = tk.Button(
    root,
    command=delete_bookings,
    text="Lemondás",
    activebackground="skyblue",
    activeforeground="white",
    anchor="center",
    bd=3,
    bg="skyblue",
    disabledforeground="grey",
    fg="black",
    font=("Arial", 12),
    height=2,
    highlightbackground="black",
    highlightcolor="green",
    highlightthickness=2,
    justify="center",
    overrelief="raised",
    padx=10,
    pady=5,
    width=15,
    wraplength=100
)

button3 = tk.Button(
    root,
    command=listing_button_click,
    text="Listázás",
    activebackground="skyblue",
    activeforeground="white",
    anchor="center",
    bd=3,
    bg="skyblue",
    disabledforeground="grey",
    fg="black",
    font=("Arial", 12),
    height=2,
    highlightbackground="black",
    highlightcolor="green",
    highlightthickness=2,
    justify="center",
    overrelief="raised",
    padx=10,
    pady=5,
    width=15,
    wraplength=100
)

foglalt_szobak_szöveg = tk.Text(
    root,
    height=10,
    width=80,
    background="gold")

hiba = tk.Text(
    root,
    height=10,
    width=80,
    background="gold")

button1.pack(padx=10, pady=10)
input.pack(padx=10, pady=10)
optionmenu.pack(padx=10, pady=10)
button2.pack(padx=20, pady=20)
button3.pack(padx=20, pady=20)
foglalt_szobak_szöveg.pack(padx=10, pady=10)
hiba.pack(padx=10, pady=10)

root.mainloop()