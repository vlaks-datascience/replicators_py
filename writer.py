import socket
from time import sleep
from writer_functions import logger
from Reader1_functions import get_last_value_for_code1
from Reader1_functions import read_values_by_code1
from Reader2_functions import get_last_value_for_code2
from Reader2_functions import read_values_by_code2
from Reader3_functions import get_last_value_for_code3
from Reader3_functions import read_values_by_code3
from Reader4_functions import get_last_value_for_code4
from Reader4_functions import read_values_by_code4


HOST = "127.0.0.1"
PORT = 8001
address = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(address)
    logger("Successfully connected to ReplicatorSender server!")

    while True:
        print("---------- MENU ----------")
        print("1. Send data to database")
        print("2. Get last value for selected code")
        print("3. Get all values for selected code")
        print("4. Exit program")

        print("Choose option by entering number:")
        option = input()

        if option == "1":
            while True:
                print("WRITER: Please input your data")
                print("To stop sending data, type -1 as Code and END as Value")

                print("Enter desired Code:")
                code = input()
                print("Enter desired Value:")
                value = input()

                if int(code) == -1 or value == "END":
                    print("Stopping writer...")
                    logger("Uneta vrednost za zaustavljanje rada writera")
                    break
                if not code.isdigit():
                    print("Code must be integer between 1 and 8")
                    logger("Uneta nevalidna vrednost za kod: non-integer")
                    break

                if 1 <= int(code) <= 8:
                    sleep(2)
                    data = str(code) + ";" + str(value)
                    s.sendall(data.encode('utf-8'))
                    logger("Uspesno poslani podaci na ReplicatorSender server!")
                    print("Writer has sent your data to the next destination")
                else:
                    print("Code must be integer between 1 and 8")
                    logger("Uneta nevalidna vrednost za kod: broj nije izmedju 1 i 8")
        elif option == "2":
            print("Enter desired code to get last value")
            kod = input()
            if kod == "1" or kod == "2":
                get_last_value_for_code1(int(kod))
            elif kod == "3" or kod == "4":
                get_last_value_for_code2(int(kod))
            elif kod == "5" or kod == "6":
                get_last_value_for_code3(int(kod))
            elif kod == "7" or kod == "8":
                get_last_value_for_code4(int(kod))
            else:
                print("Code is not recognized. Codes must be in range between 1 and 8")
        elif option == "3":
            print("Enter desired code to get all values")
            kod = input()
            if kod == "1" or kod == "2":
                read_values_by_code1(int(kod))
            elif kod == "3" or kod == "4":
                read_values_by_code2(int(kod))
            elif kod == "5" or kod == "6":
                read_values_by_code3(int(kod))
            elif kod == "7" or kod == "8":
                read_values_by_code4(int(kod))
            else:
                print("Code is not recognized. Codes must be in range between 1 and 8")
        elif option == "4":
            print("Exiting program . . .")
            break
        else:
            print("Selected option not recognized. Please try again")
    # s.close()
logger("Successfully closed writer-client!")
