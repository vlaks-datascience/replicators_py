# Uvod
- kod je pisan u python programskom jeziku
- koriscena je klient/server arhitektura sa tcp protokolom
- sastoji se od 4 komponente(writer, replicator sender, replicator receiver, reader)
- korisceni python paketi su socket, pickle, threading, time, unittest
- za bazu podataka se koristi MySQL
- prvo se pokrenu 4 readera, posle se pokrene receiver, pa sender, pa proizvoljan broj writera

## Writer komponenta
  Writer odnosno početna komponenta se koristi za uspostavljanje konekcije sa Replicator Sender komponentom. Korisnik može da bira iz menija opcije za rad:
  - 1 Slanje podataka ka bazi podataka
      - Od korisnika se traži da unese kod i vrednost koju želi da upiše u bazu podataka
  - 2 Dobijanje poslednje vrednosti za izabrani kod
      - Od korisnika se traži da unese kod za koji želi da dobije poslednju vrednost iz baze podataka
  - 3 Dobijanje svih vrednosti za izabrani kod
      - Od korisnika se traži da unese kod za koji želi da dobije sve vrednosti iz baze podataka
  - 4 Izlaz iz programa
      - Odabirom ove opcije, program se zatvara 

## Replicator sender komponenta
Replicator Sender komponenta prima podatke od writer komponente. Rucno se moze upaliti i gasiti vise writera i istovremeno se mogu slati podaci sa vise writera. Podatak kad se primi od writera se ubacuje u bafer kao jedan objekat klase ReceiverProperty ako je primljen podatak validan. Bufer je niz od 4 ColectionDescription objekata. Sender na svakih 90 sekundi salje podatke iz bufera ka Replicator Receiver komponenti.
Funkcije ko Sender koristi:
- **konvertuj_u_receiver_property(data)**
  - kao parametar prima podatak dboijen od writera
  - ako je podatak validan kreira odgovarajuci objekat ReceiverProperty klase
  - za povratnu vrednost vraca taj objekat
- **logger(tekst)**
  - kao parametar prima poruku za ispis
  - upisuje u txt fajl vreme i dogadjaj koju pporuku opisuje
  - povratna vrednost je ispis kao string
- **ubaci_u_collection_description(recProp)**
  - prima objekat klase ReceiverProperty
  - u zavisnosti od koda koji sadrzi smesta ga u odgovarajuci CollectionDescription objekat
- **ispazni_buffer()**
  - ispraznjuje buffer
- **provera_za_slanje(trenutak_pocetka_prijema)**
  - proverava da le je proslo 90 sekundi
  - ako jeste onda pravi konekciju prema Replicator Receiver komponenti
  - i salje joj podatke iz bufera
- **handle_writer(connection, addres)**
  - kao parametar prima adresu writera i njegovu konekciju
  - u beskonacnoj petlji prima podatke od writera
  - pa potom poziva funkcije konvertuj_u_receiver_property i ubaci_u_collection_description
- **start_sender_server(socket-SenderServer)**
  - kao parametar prima socket
  - u beskonacnoj petlji ceka da se writeri konektuju
  - ako se jedan writer konektuje pravi mu jedan nit

Pri pokretanju komponente, kreira se nit za provera_za_slanje funkciju. Na ovaj nacin Sender moze da prima podatke od writera a paralelno proverava da li je proslo 90 sekundi za slanje podataka iz bufera. Kad se jedan Writer konektuje kreira mu se jedna posebna nit, da bi vise Writera istovremeno moglo da salje podatke.

## Replicator Receiver komponenta
  Replicator Receiver komponenta se koristi za uspostavljanje konekcije sa Replicator Sender komponentom, od koje prima CollectionDescription objekat, i sa Reader komponentama u zavisnosti od ispunjenosti određenog uslova kojima šalje DeltaCD objekat. 

  Nakon što Receiver primi objekat, potrebno je da prođe kroz njegove atribute, i izvuče kod. Na osnovu koda, će se manipulisati sa listama add i update i to tako što će kad prvi put primi neki kod, njega staviti u add listu, a svaki naredni put u update listu.
  Pošto je raspored kodova po datasetovima već određen u prethodnoj komponenti, samo će se nadovezati te CollectionDescription1 (CD1) će se prepakovati u DeltaCD1 (DCD1) i takav poslati Reader1 komponenti. CD2 će biti prepakovan u DCD2 i poslaće se Reader2 komponenti. Na isti način će biti odrađeno za datasetove tri i četiri.

  Funkcije koje Receiver koristi:
  - **check(delt)**
    - kao parametar prima objekat DeltaCD
    - služi za proveru ispunjenosti uslova da je suma brojeva kodova u listama add i update jednaka 10
    - kao povratnu vrednost vraća True ili False
  - **send(i)**
    - kao parametar prima broj od 1 do 4
    - poziva metodu check kojoj prosleđuje jedan od objekata deltaCD zavisno od parametra i
    - uspostavlja konekciju ka Reader[1-4] komponenti i šalje deltaCD[1-4] objekat

## Reader komponenta
Reader komponenta služi da uspostavi konekciju sa Replicator Receiver komponentom, primi od nje podatke i trajno ih sačuva u bazu podataka.
Postoji 4 Reader-a od kojih svaki radi sa svojom tabelom u bazi podataka.
- Reader1
  - Radi sa dataset-om 1 i kodovima CODE_ANALOG[1] i CODE_DIGITAL[2]
- Reader2
  - Radi sa dataset-om 2 i kodovima CODE_CUSTOM[3] i CODE_LIMITSET[4]
- Reader3
  - Radi sa dataset-om 3 i kodovima CODE_SINGLENODE[5] i CODE_MULTIPLENODE[6]
- Reader4
  - Radi sa dataset-om 4 i kodovima CODE_CONSUMER[7] i CODE_SOURCE[8]

U samim Reader komponentama se nalazi uspostavljanje konekcije sa <i>Replicator Receiver</i> komponentom kako bi pridobio podatke i mogao da ih ubaci u proces ubacivanja u bazu podataka.
Za bazu podataka se koristi MySql za koji je potreban mysql-connector package.

Izgled tabele:
| ID | DATASET | CODE | VALUE | DATETIME [PK] |
| --- | --- | --- | --- | --- |
| --- | --- | --- | --- | --- |
> Ovako izgleda tabela za svakog od reader-a

Reader komponente koriste funkcije iz fajlova reader_functions koje služe za proveru pristiglih podataka, upis u bazu, i pribavljanje podataka iz baze.
Funkcije koje Reader koristi su:
- **mydb_connection(host_name, user_name, user_password)**
  - ova funkcija ima povratnu vrednost <i>connection</i> uz pomoć koje će se dalje kroz program MySql komande.
  - pored toga služi i za konekciju sa bazom podataka
- **logger(message)**
  - služi za beleženje svih aktivnosti koje se dešavaju u svakoj od reader-a.
  - za parametar prima poruku koju će ispisati u .txt fajlu zajedno sa vremenom u koje vreme se neka funkcija izvršavala.
- **connect_to_database()**
  - služi da bi se napravila ako već ne postoji baza podataka u koju ce se smeštati kasnije dobijeni podaci.
- **create_table()**
  - služi za pravljenje tabele za svaku od reader-a, ukoliko vec ne postoji.
- **insert_process(id, dataset, code, value)**
  - koristi se na dobijenim podacima kako bi izvrsila proveru i validnost podataka
- **check_deadband(id, dataset, code, value)**
  - služi za proveru podataka koji već postoje u bazi sa unetom vrednošću, ukoliko postoji vec slična vrednost sa istim kodom, ona se zanemaruje, u suprotnom se šalje na upis.
- **insert(id, dataset, code, value)**
  - nakon svih prethodno izvršenih provera, funkcija insert služi za upis podataka (id, dataset, code, value, datetime) u određenu tabelu u bazi podataka.
- **get_last_value_for_code(code)**
  - koristi se kako bi ispisala poslednju unetu vrednost u bazi podataka za uneti kod.
- **read_values_by_code(code)**
  - funkcija koja dobavlja i ispisuje sve vrednosti iz tabele za određeni Reader za uneti kod. 
- **get_fetchall(cursor)**
  - funkcija koja služi za skraćivanje koda i lakšeg testiranja koda 

## Codovi Enumeracija

- U ovom fajlu se nalazi enumeracija za kodove:
    - CODE_ANALOG = 1
    - CODE_DIGITAL = 2
    - CODE_CUSTOM = 3
    - CODE_LIMITSET = 4
    - CODE_SINGLENODE = 5
    - CODE_MULTIPLENODE = 6
    - CODE_CONSUMER = 7
    - CODE_SOURCE = 8

## ReceiverProperty klasa
- Klasa sadrži polja Code i Value
- Propertiji koji su implementirani:
  - get_code() - vraća kod datog objekta
  - get_value() - vraća vrednost datog objekta

## HistoricalCollection klasa
- Klasa sadrži niz ReceiverProperty-ja
- Metode koje su implementirane:
  - dodaj(a) - dodaje prosleđeni parametar a u niz
  - isprazni() - prazni niz
  - get_niz() - vraća niz

## CollectionDescription klasa
- Klasa sadrži polja id, dataset, historicalCollection objekat
- Metode koje su implementirane:
  - get_id() - vraća id za dati objekat klase
  - get_dataset() - vraća dataset za dati objekat klase
  - get_historical_collection() - vraća historicalCollection objekat za dati objekat klase
  - dodaj_u_historical_collection(cd) - poziva metodu dodaj iz HistoricalCollection klase kojoj prosleđuje cd kao parametar
  - isprazni_historical_collection() - poziva metodu isprazni iz HistoricalCollection klase

## DeltaCD klasa
- Klasa sadrži polja add_list i update_list
- Metode koje su implementirane:
  - dodaj_novi(cd) - prosleđeni objekat cd dodaje u svoju add listu
  - azuriraj_postojeci(cd) - prosleđeni objekat cd dodaje u svoju update listu
