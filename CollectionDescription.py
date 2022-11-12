import historicalCollection


class CollectionDescription:
    def __init__(self, id_, data_set):
        self.id = id_
        self.data_set = data_set
        self.historical_collection = historicalCollection.HistoricalCollection()

    def dodaj_u_historical_collection(self, cd):
        self.historical_collection.dodaj(cd)

    def isprazni_historical_collection(self):
        self.historical_collection.isprazni()

    def get_id(self):
        return self.id

    def get_dataset(self):
        return self.data_set

    def get_historical_collection(self):
        return self.historical_collection
