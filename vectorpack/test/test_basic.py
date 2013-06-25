import unittest

from numpy import array

from vectorpack import packs

#print packs.pack_first_fit_by_items(items=items, boxes=boxes, 
#                                   item_key=lambda i: -sum(i))
#print packs.pack_first_fit_by_boxes(items=items, boxes=boxes, 
#                                   item_key=lambda i: -sum(i))
#print packs.pack_select_by_items(items=items, boxes=boxes, 
#                                item_key=lambda i: -sum(i),
#                                match_key=lambda i, c: sum(c - i))
#print packs.pack_select_by_boxes(items=items, boxes=boxes, 
#                                match_key=lambda i, c: sum(c - i))


#print packs.pack_select_by_items(items=items, boxes=boxes, item_key=lambda i: -sum(i),
#                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))
#print packs.pack_select_by_boxes(items=items, boxes=boxes, box_key=sum,
#                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))

#print packs.pack_first_fit_by_boxes(items=items, boxes=boxes)
#print packs.pack_select_by_items(items=items, boxes=boxes)
#print packs.pack_select_by_boxes(items=items, boxes=boxes)


# FIXME: move to util.py?
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
    
    def test_first_fit_by_items(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            packs.pack_first_fit_by_items(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            packs.pack_first_fit_by_items(items=items, boxes=boxes, 
                                          item_key=lambda i: -sum(i)),
            [0, 2, 2, 1])

    def test_first_fit_by_boxes(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            packs.pack_first_fit_by_boxes(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            packs.pack_first_fit_by_boxes(items=items, boxes=boxes, 
                                          item_key=lambda i: -sum(i)),
            [0, 2, 2, 1])

    def test_best_fit_by_items(self):
        items = [array([1, 1]), array([2, 2]), array([2, 1]), array([1, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            packs.pack_best_fit_by_items(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            packs.pack_best_fit_by_items(items=items, boxes=boxes, 
                                          select_key=lambda i, c: sum(c - i)),
            [0, 1, 2, 2])

    def test_best_fit_by_boxes_no_sorts(self):
        items = [array([1, 1]), array([2, 2]), array([2, 1]), array([1, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            packs.pack_best_fit_by_boxes(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            packs.pack_best_fit_by_boxes(items=items, boxes=boxes, 
                                          select_key=lambda i, c: sum(c - i)),
            [0, 1, 2, 2])

    def test_best_fit_no_sorts(self):
        items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
        boxes = [array([6, 6])]
        self.assertEqual(
            packs.pack_best_fit(items=items, boxes=boxes),
            [0, 0, 0, 0])
        boxes = [array([1, 1]), array([2, 2]), array([3, 3])]
        self.assertEqual(
            packs.pack_best_fit(items=items, boxes=boxes, 
                                          select_key=lambda i, c: sum(c - i)),
            [0, 2, 2, 1])
         

def main():
    unittest.main()

if __name__ == '__main__':
    main()
