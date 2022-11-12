import unittest
import historicalCollection
import receiverProperty


class TestHistoricalCollection(unittest.TestCase):
    def test_getNiz(self):
        hc = historicalCollection.HistoricalCollection()
        rc = receiverProperty.ReceiverProperty(1, 234)
        hc.dodaj(rc)
        niz = []
        niz.append(rc)
        self.assertEqual(historicalCollection.HistoricalCollection.get_niz(hc), niz)


if __name__ == '__main__':
    unittest.main()
