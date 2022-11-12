# Reader3-server.py
import pickle
import socket
from Reader3_functions import logger
from Reader3_functions import connect_to_database
from Reader3_functions import create_table
from Reader3_functions import insert_process

HOST_R3 = "127.0.0.1"
PORT_R3 = 8007
NUMBER_OF_BYTES = 1000000

connect_to_database()
logger("Reader3 successfully connected to database.")
create_table()

# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST_R3, PORT_R3))
    while True:
        s.listen()
        print("Reader3: Waiting for connection...")
        logger("Reader3 waiting for connection.")
        conn, addr = s.accept()
        print(f"Reader3: Replicator receiver connected from {addr}")
        logger("ReplicatorReceiver successfully connected to Reader3.")
        inc_data = conn.recv(NUMBER_OF_BYTES)
        data = pickle.loads(inc_data)
        logger("Reader3 successfully received data from replicatorReceiver.")
        add_lista = data.add_list
        update_lista = data.update_list
        # upisivanje vrednosti u tabelu iz add_list-e
        logger("Reader3 started reading data from add_list.")
        for cdx in add_lista:
            id_add = cdx.get_id()
            dataset_add = cdx.get_dataset()
            hc_add = cdx.get_historical_collection().get_niz()
            for cdy in hc_add:
                code_add = cdy.get_code()
                value_add = cdy.get_value()
                insert_process(id_add, dataset_add, code_add, value_add)

        # upisivanje vrednosti u tabelu iz update_list-e
        logger("Reader1 started reading data from update_list.")
        for cdx in update_lista:
            id_update = cdx.get_id()
            dataset_update = cdx.get_dataset()
            hc_update = cdx.get_historical_collection().get_niz()
            for cdy in hc_update:
                code_update = cdy.get_code()
                value_update = cdy.get_value()
                insert_process(id_update, dataset_update, code_update, value_update)
        conn.close()
