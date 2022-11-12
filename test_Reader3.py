import unittest
from time import localtime
from unittest.mock import patch
from Reader3_functions import logger, check_deadband, insert, get_last_value_for_code3, read_values_by_code3
from Reader3_functions import insert_process, create_table, connect_to_database

id_err = "ID is not valid!"
value_err = "Value is not valid!"
code_err = "Code is not in range 5:6!"
int_err = "Code is not integer!"


class TestLogger(unittest.TestCase):
    def test_logger_characters(self):
        time_now = localtime()
        message = "Just trying"
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")

    def test_logger_numbers(self):
        time_now = localtime()
        message = 1.15
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")

    def test_logger_null(self):
        time_now = localtime()
        message = None
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")

    def test_logger_empty_string(self):
        time_now = localtime()
        message = ""
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")


# testovi za insert_process
class TestInsertProcess(unittest.TestCase):
    @patch('Reader3_functions.check_deadband')
    def test_process__good__code_singlenode(self, mock_check):
        mock_check.return_value = "Ulazi dalje u check_deadband"
        self.assertEqual(insert_process(3, 3, 5, 100), mock_check.return_value)

    @patch('Reader3_functions.check_deadband')
    def test_process__good__code_multiplenode(self, mock_check_deadband):
        mock_check_deadband.return_value = "Ulazi dalje u check_deadband"
        self.assertEqual(insert_process(3, 3, 6, 100), mock_check_deadband.return_value)

    def test_process_bad_id(self):
        self.assertEqual(insert_process("not int", 3, 6, 100), id_err)

    def test_process_bad_id2(self):
        self.assertEqual(insert_process(None, 3, 6, 100), id_err)

    def test_process_bad_id3(self):
        self.assertEqual(insert_process(1.33, 3, 6, 100), id_err)

    def test_process_bad_value(self):
        self.assertEqual(insert_process(3, 3, 5, 214748364799), value_err)

    def test_process_bad_value2(self):
        self.assertEqual(insert_process(3, 3, 5, -214748364799), value_err)

    def test_process_bad_dataset(self):
        self.assertEqual(insert_process(3, 1, 5, 100), "Dataset is not valid!")

    def test_process_bad_dataset2(self):
        self.assertEqual(insert_process(3, None, 6, 100), "Dataset is not valid!")

    def test_process_bad_code(self):
        self.assertEqual(insert_process(3, 3, 1, 100), code_err)

    def test_process_bad_code2(self):
        self.assertEqual(insert_process(3, 3, None, 100), int_err)


# testovi za check_deadband
class TestCheckDeadband(unittest.TestCase):
    @patch('Reader3_functions.get_fetchall')
    @patch('Reader3_functions.insert')
    def test_check_doesnt_exist(self, mock_insert, mock_get_fetchall):
        mock_insert.return_value = "INSERT"
        mock_get_fetchall.return_value = None
        self.assertEqual(check_deadband(3, 3, 'CODE_SINGLENODE', 100), "INSERT")

    @patch('Reader3_functions.get_fetchall')
    @patch('Reader3_functions.insert')
    def test_check_does_exist(self, mock_insert, mock_get_fetchall):
        mock_insert.return_value = "INSERT"
        mock_get_fetchall.return_value = [(10000,)]
        # namerno 10000 da bi razlika bila veca od 2%
        self.assertEqual(check_deadband(3, 3, 'CODE_MULTIPLENODE', 100), "INSERT")

    @patch('Reader3_functions.get_fetchall')
    @patch('Reader3_functions.insert')
    def test_check_no_insert(self, mock_insert, mock_get_fetchall):
        mock_insert.return_value = "INSERT"
        mock_get_fetchall.return_value = [(100,)]
        # namerno 100 da bi razlika bila tacno 0 sto je manje od 2%
        self.assertEqual(check_deadband(3, 3, 'CODE_SINGLENODE', 100), None)


# testovi za insert
class TestInsert(unittest.TestCase):
    def test_insert1(self):
        self.assertEqual(insert(3, 3, 'CODE_SINGLENODE', 10000), "Inserted successfully!")

    def test_insert2(self):
        self.assertEqual(insert(3, 3, 'CODE_MULTIPLENODE', 10000), "Inserted successfully!")


class TestGetLast(unittest.TestCase):
    def test_code_not_int(self):
        self.assertEqual(get_last_value_for_code3(None), int_err)

    def test_code_not_5or6(self):
        self.assertEqual(get_last_value_for_code3(1), code_err)

    @patch('Reader3_functions.get_fetchall')
    def test_code_doesnt_exist(self, mock_get_fetchall):
        connect_to_database()
        create_table()
        mock_get_fetchall.return_value = None
        self.assertEqual(get_last_value_for_code3(5), "Code doesnt exist")

    @patch('Reader3_functions.get_fetchall')
    def test_code_exists(self, mock_get_fetchall):
        create_table()
        mock_get_fetchall.return_value = [(3, 3, 'CODE_SINGLENODE', 10000, (2022, 6, 21, 13, 26, 3))]
        self.assertEqual(get_last_value_for_code3(5), "Exists, printed")


class TestReadValues(unittest.TestCase):
    def test_code_not_int(self):
        self.assertEqual(read_values_by_code3(None), int_err)

    def test_code_not_5or6(self):
        self.assertEqual(read_values_by_code3(1), code_err)

    @patch('Reader3_functions.get_fetchall')
    def test_code_doesnt_exist(self, mock_get_fetchall):
        mock_get_fetchall.return_value = None
        self.assertEqual(read_values_by_code3(5), "Code doesnt exist")

    @patch('Reader3_functions.get_fetchall')
    def test_code_exists(self, mock_get_fetchall):
        mock_get_fetchall.return_value = [(3, 3, 'CODE_MULTIPLENODE', 10000, (2022, 6, 21, 13, 26, 3))]
        self.assertEqual(read_values_by_code3(6), "Exists, printed")


if __name__ == '__main__':
    unittest.main()
