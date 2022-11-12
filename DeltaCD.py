# DeltaCD.py

class DeltaCD:
    def __init__(self):
        self.add_list = []   # Lista u kojoj se nalaze objekti CD koji trebaju da se dodaju u bazu
        self.update_list = []    # Lista u kojoj se nalaze objekti CD koji trebaju da se azuriraju u bazi

    def dodaj_novi(self, cd):
        self.add_list.append(cd)
    
    def azuriraj_postojeci(self, cd):
        self.update_list.append(cd)
