class HistoricalCollection:
    def __init__(self):
        self.niz_receiver_property = []

    def dodaj(self, a):
        self.niz_receiver_property.append(a)
    
    def isprazni(self):
        self.niz_receiver_property.clear()

    def get_niz(self):
        return self.niz_receiver_property
