import unittest

from numpy import array

from vectorpack import leinberger

class LeinbergerBasicTests(unittest.TestCase):
    
    def test_permutation_pack(self):
        items = [array([1, 1]), array([2, 2]), array([2, 1]), array([1, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            leinberger.permutation_pack(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            leinberger.permutation_pack(items=items, boxes=boxes),
            [0, 1, 2, 2])
         
    def test_choose_pack(self):
        items = [array([1, 1]), array([2, 2]), array([2, 1]), array([1, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            leinberger.choose_pack(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            leinberger.choose_pack(items=items, boxes=boxes),
            [0, 1, 2, 2])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
