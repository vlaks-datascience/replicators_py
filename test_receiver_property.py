import unittest
import receiverProperty


class TestProperty(unittest.TestCase):
    def test_get_code(self):
        rp = receiverProperty.ReceiverProperty(1, 123)
        self.assertEqual(receiverProperty.ReceiverProperty.get_code(rp), 1)

    def test_get_value(self):
        rp = receiverProperty.ReceiverProperty(1, 123)
        self.assertEqual(receiverProperty.ReceiverProperty.get_value(rp), 123)
        

if __name__ == '__main__':
    unittest.main()
