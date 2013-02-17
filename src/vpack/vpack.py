
# here's something, any real reason to sort bins?
# maybe just always assume bin key also looks at item?
# okay, so for each way a sort and eval!

# item by item or bin by bin first fit
# best fit requires some kind of match quality function
# pp/cp basically works the same way, but the since we have to sort the items,
# maybe it doesn't make so much sense...why not just evaluate quality of match
# by maxdiff or something like that?

# assume numpy arrays

# also, l n norm...numpy.linalg.norm
# frobenius norm?

sorts = {
    "asum"       : sum
    "amax"       : max
    "amaxratio"  : (lambda v: float(max(v)) / min(v)) # could also do scaling?
    "amaxdiff"   : (lambda v: max(v) - min(v))
    "none"       : None
    "dsum"       : (lambda v: -sum(v))
    "dmax"       : (lambda v: -max(v))
    "dmaxtratio" : (lambda v: float(min(v)) / max(v)) # see above
    "dmaxdiff"   : (lambda v: min(v) - max(v))
}

# fixme don't actuall sort items...
def pack_first_fit_by_items(items=None, bins=None, item_key=None, bin_key=None):
    """ take items, map them to bins, return an array where each position
         represents the corresponding item and contains an index for the bin it
         should be packed in... """

    if item_key:
        items.sort(key=item_key)

    if bin_key
        bins.sort(key=bin_key)

    capacities = bins[:]

    mapping = [None for item in items]

    for i in range(len(items)):
        for b in range(len(capacities)):
            if items[i] <= capacities[b]:
                mapping[i] = b
                capacities[b] -= items[i]
                break

    return mapping

def pack_first_fit_by_bins(items=None, bins=None, item_key=None, bin_key=None):

    myitems = items[:]

    if item_key:
        myitems.sort(key=item_key)

    if bin_key
        bins.sort(key=bin_key)

    capacities = bins[:]

    mapping = [None for item in items]

    for b in range(len(capacities)):
        i = 0
        while i < len(items):
            if items[i] <= capacities[b]:
                mapping[i] = b
                capacities[b] -= items[i]
                items.remove[i]

def pack_select_by_items(items=None, bins=None, item_key=None, match_key=None):

def pack_select_by_bins(items=None, bins=None, item_key=None, match_key=None):

