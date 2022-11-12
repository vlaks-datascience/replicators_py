import socket
import pickle
import DeltaCD
from replicatorReceiver_functions import logger

HOST = "127.0.0.1" 
PORT0 = 8002    # server port
PORT1 = 8005    # client port for reader1
PORT2 = 8006    # client port for reader2
PORT3 = 8007    # client port for reader3
PORT4 = 8008    # client port for reader4
BROJ_BAJTOVA_KOJI_SE_PRIMA = 1000000

address0 = (HOST, PORT0)
address1 = (HOST, PORT1)
address2 = (HOST, PORT2)
address3 = (HOST, PORT3)
address4 = (HOST, PORT4)


buffer = []
delta_cd = []
address = []
kodovi = []
address.append(address1)
address.append(address2)
address.append(address3)
address.append(address4)

delta_cd1 = DeltaCD.DeltaCD()
delta_cd2 = DeltaCD.DeltaCD()
delta_cd3  = DeltaCD.DeltaCD()
delta_cd4 = DeltaCD.DeltaCD()

delta_cd.append(delta_cd1)
delta_cd.append(delta_cd2)
delta_cd.append(delta_cd3)
delta_cd.append(delta_cd4)


def check(delt):
    if len(delt.add_list) + len(delt.update_list) == 10:
        return True
    else:
        return False


def send(i):
    if check(delta_cd[i]):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address[i])
                msg = pickle.dumps(delta_cd[i])  
                replicatorReceiverClient.send(msg)
                i += 1
                logger("Uspesno poslani podaci na Reader {i}!")


# socket za primanje podataka
replicatorReceiverServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorReceiverServer.bind(address0)
replicatorReceiverServer.listen()
print("Cekanje na konekciju...")
logger("Uspesno otvoren server za osluskivanje!")


while True:
    conn, addr = replicatorReceiverServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA)
    buffer = pickle.loads(data)
    logger("Uspesno primljeni podaci na server!")

    i = 0
    for delta in delta_cd:


        id_iz_buff = buffer[i].get_id()
        dataset_iz_buff = buffer[i].get_dataset()
        for y in buffer[i].get_historical_collection().get_niz():
            code_iz_buff = y.get_code()
            value_iz_buff = y.get_value()
            if code_iz_buff not in kodovi:
                delta.dodaj_novi(buffer[i])
                kodovi.append(code_iz_buff)
                logger("Uspesno dodan novi kod u add listu!")
            else:
                delta.azuriraj_postojeci(buffer[i])
                logger("Uspesno dodan vec postojeci kod u update listu!")
        i += 1

    #for k in range (0, 4):
        #send(k)



    if(len(delta_cd1.add_list) + len(delta_cd1.update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address1)
                msg = pickle.dumps(delta_cd1)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 1!")
                delta_cd1.add_list.clear()
                delta_cd1.update_list.clear()
                logger("Liste za deltaCD1 ispraznjene!")



    if(len(delta_cd2.add_list) + len(delta_cd2.update_list) == 10):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address2)
                msg = pickle.dumps(delta_cd2)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 2!")
                delta_cd2.add_list.clear()
                delta_cd2.update_list.clear()
                logger("Liste za deltaCD2 ispraznjene!")

    if(len(delta_cd3.add_list) + len(delta_cd3.update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address3)
                msg = pickle.dumps(delta_cd3)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 3!")
                delta_cd3.add_list.clear()
                delta_cd3.update_list.clear()
                logger("Liste za deltaCD3 ispraznjene!")

    if(len(delta_cd4.add_list) + len(delta_cd4.update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address4)
                msg = pickle.dumps(delta_cd4)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 4!")
                delta_cd4.add_list.clear()
                delta_cd4.update_list.clear()
                logger("Liste za deltaCD4 ispraznjene!")
    
