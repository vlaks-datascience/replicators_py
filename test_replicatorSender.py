import unittest
import time
from sender_functions import konvertuj_u_receiver_property
from sender_functions import logger


class TestSender(unittest.TestCase):
    def test_Logger(self):
        vreme = time.localtime()
        self.assertEqual(logger("poruka"), f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, "
                                           f"{vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, " + "poruka"+"\n")
        self.assertEqual(logger(3), f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, "
                                    f"{vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, {3}\n")
        self.assertEqual(logger(object), f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, "
                                         f"{vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, {object}\n")

    def test_konvertuj_u_ReceiverProperty(self):
        self.assertEqual(konvertuj_u_receiver_property(""), "lose")
        self.assertEqual(konvertuj_u_receiver_property(3), "lose")
        self.assertEqual(konvertuj_u_receiver_property(5.77), "lose")
        self.assertEqual(konvertuj_u_receiver_property(object), "lose")
        self.assertEqual(konvertuj_u_receiver_property("3;3;"), "lose")


if __name__ == '__main__':
    unittest.main()
