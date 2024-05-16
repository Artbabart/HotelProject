class Hotel:
    bookings = []  # Osztályváltozóként tároljuk a foglalásokat

    def __init__(self, name, booking):
        self.name = name
        self.foglalas = booking

    def __str__(self) -> str:
        return f"a szalloda neve: {self.name}"

    def __add__(self, room):
        self.bookings.append(room)

    def Booking(self):
        print("Foglalt szobák:")
        for room in self.bookings:
            print(f"Szoba száma: {room.id}, Szoba típusa: {room.type}, Szoba ára: {room.price}")