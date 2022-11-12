import unittest
import time
from replicatorReceiver_functions import logger


class TestLogg(unittest.TestCase):
    def test_logger(self):
        time_now = time.localtime()
        self.assertEqual(logger("proba"), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, proba\n")
        self.assertEqual(logger(6), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                    f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, 6\n")
        self.assertEqual(logger(""), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                     f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, \n")
        self.assertEqual(logger(object), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                         f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, {object}\n")


if __name__ == '__main__':
    unittest.main()
