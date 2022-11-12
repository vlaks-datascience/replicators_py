import mysql.connector
from time import localtime, sleep
import codovi

codenotint = "Code is not integer!"
message1 = f"Reader2: {codenotint}"
codenotrange = "Code is not in range 3:4!"
message2 = f"Reader2: {codenotrange}"


def logger(message):
    time_now = localtime()
    with open("Reader2_Logger.txt", 'a') as file:
        log = f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, " \
            f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}" \
            f" -> {message}\n"
        file.write(f"{log}")
        file.close()
        return log


def get_fetchall(mycursor):
    return mycursor.fetchall()


# kreiranje DATABASE database_reader ako ne postoji
def connect_to_database():
    sqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root")
    mycur = sqldb.cursor()
    mycur.execute("SELECT IF(EXISTS( SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
                  " WHERE SCHEMA_NAME = 'database_reader'), 'Yes', 'No') as exist")
    myresult = mycur.fetchone()
    if myresult[0] == "Yes":
        logger("Reader2 tried to create database that already exists, attempting to connect.")
        return print("Reader2: Database database_reader already exists, attempting to connect...")
    else:
        mycur.execute("create database database_reader")
        logger("Reader2 successfully created database: [database_reader].")
        return print("Reader2: Creating database database_reader")


# kreiranje tabele za reader2 ako ne postoji
def create_table():
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata2'")
    myresult = mycursor.fetchall()
    if not myresult:
        mycursor.execute("create table tabledata2(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        logger("Reader2 successfully created table: [tabledata2].")
        print("Reader2: Creating tabledata2")
        return "Table created and ready to use!"
    else:
        print("Reader2: Table tabledata2 already exists, ready to use")
        return "Table ready to use!"


# funkcija koja proverava da li je code code_digital
def insert_process(id_data, dataset, code_number, value):
    message = "Reader2 successfully executed function: [insert_process]."
    if not isinstance(code_number, int):
        print(message1)
        logger(message)
        return codenotint
    elif code_number != 3 and code_number != 4:
        print(message2)
        logger(message)
        return codenotrange
    code = codovi.Code(code_number).name
    if not isinstance(id_data, int):
        print("Reader2: ID is not valid!")
        logger(message)
        return "ID is not valid!"
    elif value >= 2147483647 or value <= -2147483648:
        print("Reader2: Value is not valid!")
        logger(message)
        return "Value is not valid!"
    elif dataset != 2:
        print("Reader2: Dataset is not valid!")
        logger(message)
        return "Dataset is not valid!"
    else:
        print(f"Reader2: Checking deadband for code [{code}]...")
        logger(message)
        return check_deadband(id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(id_data, dataset, code, value):
    message = "Reader2 successfully executed function: [check_deadband]."
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata2 where code = '{code}'")
    myresult = get_fetchall(mycursor)
    if not myresult:
        print("Reader2: Code does not exist in table, inserting data")
        logger(message)
        return insert(id_data, dataset, code, value)
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i == myresult.__len__():
        print(f"Reader2: Difference between {value} and values in database is "
              f"greater than 2%, inserting data into table tabledata2")
        logger(message)
        return insert(id_data, dataset, code, value)
    else:
        logger(message)
        return print("Reader2: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata2(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    connection.commit()
    logger("Reader2 successfully executed function: [insert].")
    sleep(1)
    return "Inserted successfully!"


# funkcija za dobavljanje poslednje vrednosti za izabrani code
def get_last_value_for_code2(code_number):
    message = "Reader2 successfully executed function: [get_last_value_for_code]."
    mycursor = connection.cursor()
    if not isinstance(code_number, int):
        print(message1)
        logger(message)
        return codenotint
    elif code_number != 3 and code_number != 4:
        print(message2)
        logger(message)
        return codenotrange
    code = codovi.Code(code_number).name
    mycursor.execute(
        f"select * from tabledata2 where date = (select max(date) from tabledata2 where code = '{code}');")
    myresult = get_fetchall(mycursor)
    if not myresult:
        print(f"Reader2: Given code ['{code}'] does not exist in the table")
        logger(message)
        return "Code doesnt exist"
    else:
        print(f"Reader2: For CODE: [{myresult[0][2]}], the latest VALUE: [{myresult[0][3]}]")
        logger(message)
        return "Exists, printed"


# ispis vrednosti za trazeni code
def read_values_by_code2(code_number):
    message = "Reader2 successfully executed function: [read_values_by_code]."
    if not isinstance(code_number, int):
        print(message1)
        logger(message)
        return codenotint
    elif code_number != 3 and code_number != 4:
        print(message2)
        logger(message)
        return codenotrange
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata2 where code = '{code}'")
    myresult = get_fetchall(mycursor)
    if not myresult:
        print(f"Reader2: Given code ['{code}'] does not exist in the table")
        logger(message)
        return "Code doesnt exist"
    else:
        print("Reader2: ID |///| DATASET |///| CODE              |///| VALUE |///| DATE       TIME")
        for x in myresult:
            print(f'Reader2: {f"{x[0]}":<9}{f"{x[1]}":<14}{f"{x[2]}":<24}{f"{x[3]}":<12}{f"{x[4]}":<10}')
        logger(message)
        return "Exists, printed"


# povezivanje na DATABASE database_reader
def mydb_connection(host_name, user_name, user_password):
    connect = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database="database_reader",
        buffered=True
    )
    print("Reader2: Connection to MySQL Database database_reader successful")
    return connect


connection = mydb_connection("localhost", "root", "root")
