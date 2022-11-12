import unittest
import CollectionDescription


class TsetColl(unittest.TestCase):
    def test_get_id(self):
        cd = CollectionDescription.CollectionDescription(1, 1)
        self.assertEqual(CollectionDescription.CollectionDescription.get_id(cd), 1)
        cd = CollectionDescription.CollectionDescription("string", 1)
        self.assertEqual(CollectionDescription.CollectionDescription.get_id(cd), "string")
        cd = CollectionDescription.CollectionDescription(None, 1)
        self.assertEqual(CollectionDescription.CollectionDescription.get_id(cd), None)
        cd = CollectionDescription.CollectionDescription(object, 1)
        self.assertEqual(CollectionDescription.CollectionDescription.get_id(cd), object)

    def test_get_dataset(self):
        cd = CollectionDescription.CollectionDescription(1, 1)
        self.assertEqual(CollectionDescription.CollectionDescription.get_dataset(cd), 1)
        cd = CollectionDescription.CollectionDescription(1, "string")
        self.assertEqual(CollectionDescription.CollectionDescription.get_dataset(cd), "string")
        cd = CollectionDescription.CollectionDescription(1, None)
        self.assertEqual(CollectionDescription.CollectionDescription.get_dataset(cd), None)
        cd = CollectionDescription.CollectionDescription(1, object)
        self.assertEqual(CollectionDescription.CollectionDescription.get_dataset(cd), object)


if __name__ == '__main__':
    unittest.main()
