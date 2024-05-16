class Room:
    def __init__(self, id, type, date, price):
        self.id = id
        self.type = type
        self.date = date
        self.price = price

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "date" : self.date,
            "ar": self.price
        }

class OneBadRoom(Room):
    def __init__(self, id, rnumber,date, price):
        super().__init__(id, rnumber, date, price)
        self.tipus = "egyagyas"
        self.ar = None

class Ketagyas(Room):
    def __init__(self, id, rnumber,date, price):
        super().__init__(id, rnumber, date, price)
        self.tipus = "ketagyas"
        self.ar = None
