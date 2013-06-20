#import pyximport; pyximport.install()
from numpy import array
from functools import partial
from sys import argv

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import util

items = [array([1, 1]), array([1, 2]), array([2, 1]), array([2, 2])]
boxes = [array([6, 6])]

print util.pack_first_fit_by_items(items=items, boxes=boxes)
print util.pack_first_fit_by_boxes(items=items, boxes=boxes)
print util.pack_select_by_items(items=items, boxes=boxes)
print util.pack_select_by_boxes(items=items, boxes=boxes)

boxes = [array([1, 1]), array([2, 2]), array([3, 3])]

print util.pack_first_fit_by_items(items=items, boxes=boxes)
print util.pack_first_fit_by_boxes(items=items, boxes=boxes)
print util.pack_select_by_items(items=items, boxes=boxes)
print util.pack_select_by_boxes(items=items, boxes=boxes)

print util.pack_first_fit_by_items(items=items, boxes=boxes, 
                                   item_key=lambda i: -sum(i))
print util.pack_first_fit_by_boxes(items=items, boxes=boxes, 
                                   item_key=lambda i: -sum(i))
print util.pack_select_by_items(items=items, boxes=boxes, 
                                item_key=lambda i: -sum(i),
                                match_key=lambda i, c: sum(c - i))
print util.pack_select_by_boxes(items=items, boxes=boxes, 
                                match_key=lambda i, c: sum(c - i))


ppw1_key = partial(util.match_dimorder, 1)
print util.pack_select_by_items(items=items, boxes=boxes, item_key=lambda i: -sum(i),
                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))
print util.pack_select_by_boxes(items=items, boxes=boxes, box_key=sum,
                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))

data = load(open(argv[1], 'r'), Loader=Loader)
boxes = data['boxes']
items = data['items']

print util.pack_first_fit_by_items(items=items, boxes=boxes, 
                                   item_key=lambda i: -sum(i))
print util.pack_first_fit_by_boxes(items=items, boxes=boxes, 
                                   item_key=lambda i: -sum(i))
print util.pack_select_by_items(items=items, boxes=boxes, 
                                item_key=lambda i: -sum(i),
                                match_key=lambda i, c: sum(c - i))
print util.pack_select_by_boxes(items=items, boxes=boxes, 
                                match_key=lambda i, c: sum(c - i))
print util.pack_select_by_items(items=items, boxes=boxes, item_key=lambda i: -sum(i),
                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))
print util.pack_select_by_boxes(items=items, boxes=boxes, box_key=sum,
                                match_key=lambda i, c: (ppw1_key(i, c), sum(c - i)))
