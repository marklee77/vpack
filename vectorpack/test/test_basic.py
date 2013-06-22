import unittest
from numpy import array
from functools import partial
from vectorpack import util


#print util.pack_first_fit_by_items(items=items, boxes=boxes)
#print util.pack_first_fit_by_boxes(items=items, boxes=boxes)
#print util.pack_select_by_items(items=items, boxes=boxes)
#print util.pack_select_by_boxes(items=items, boxes=boxes)

#print util.pack_first_fit_by_items(items=items, boxes=boxes, 
#                                   item_key=lambda i: -sum(i))
#print util.pack_first_fit_by_boxes(items=items, boxes=boxes, 
#                                   item_key=lambda i: -sum(i))
#print util.pack_select_by_items(items=items, boxes=boxes, 
#                                item_key=lambda i: -sum(i),
#                                match_key=lambda i, c: sum(c - i))
#print util.pack_select_by_boxes(items=items, boxes=boxes, 
#                                match_key=lambda i, c: sum(c - i))


# boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
#ppw1_key = partial(util.match_dimorder, 1)
#print util.pack_select_by_items(items=items, boxes=boxes, item_key=lambda i: -sum(i),
#                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))
#print util.pack_select_by_boxes(items=items, boxes=boxes, box_key=sum,
#                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))

#print util.pack_first_fit_by_boxes(items=items, boxes=boxes)
#print util.pack_select_by_items(items=items, boxes=boxes)
#print util.pack_select_by_boxes(items=items, boxes=boxes)

def verify_map(mapping, items, boxes):
    if not boxes:
        return False
    allocs = [array([0] * len(box)) for box in boxes]
    for i in range(mapping):
        allocs[mapping[i]] += items[i]
    if ((alloc <= capacity).all() for alloc, capacity in zip(allocs, boxes)).all():
        return True
    return False


class BasicTests(unittest.TestCase):
    
    def test_first_fit_by_items_no_sorts(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            util.pack_first_fit_by_items(items=items, boxes=boxes),
            [0, 0, 0, 0])

    def test_first_fit_by_boxes_no_sorts(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            util.pack_first_fit_by_boxes(items=items, boxes=boxes),
            [0, 0, 0, 0])

    def test_best_fit_by_items_no_sorts(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            util.pack_best_fit_by_items(items=items, boxes=boxes),
            [0, 0, 0, 0])

    def test_best_fit_by_boxes_no_sorts(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            util.pack_best_fit_by_boxes(items=items, boxes=boxes),
            [0, 0, 0, 0])

    def test_best_fit_no_sorts(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            util.pack_best_fit(items=items, boxes=boxes),
            [0, 0, 0, 0])
         

def main():
    unittest.main()

if __name__ == '__main__':
    main()
