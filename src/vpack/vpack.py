
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
    "asum"       : sum,
    "amax"       : max,
    "amaxratio"  : (lambda v: float(max(v)) / min(v)), # could also do scaling?
    "amaxdiff"   : (lambda v: max(v) - min(v)),
    "none"       : None,
    "dsum"       : (lambda v: -sum(v)),
    "dmax"       : (lambda v: -max(v)),
    "dmaxtratio" : (lambda v: float(min(v)) / max(v)), # see above
    "dmaxdiff"   : (lambda v: min(v) - max(v))
}

# fixme don't actuall sort items...
def pack_first_fit_by_items(items=None, bins=None, item_key=None, bin_key=None):
    """ take items, map them to bins, return an array where each position
         represents the corresponding item and contains an index for the bin it
         should be packed in... """

    item_idxs = range(len(items))
    bin_idxs = range(len(bins))

    if item_key:
        items_idxs.sort(key=lambda i: item_key(items[i]))

    if bin_key:
        bin_idxs.sort(key=lambda b: bin_key(bins[b]))

    capacities = bins[:]

    mapping = [None] * len(items)

    for i in item_idxs:
        try:
            b = next(b for b in bin_idxs if items[i] <= capacities[b])
            mapping[i] = b
            capacities[b] -= items[i]
        except StopIteration:
            return None

    return mapping

def pack_first_fit_by_bins(items=None, bins=None, item_key=None, bin_key=None):

    item_idxs = range(len(items))
    bin_idxs = range(len(bins))

    if item_key:
        items_idxs.sort(key=lambda i: item_key(items[i]))

    if bin_key:
        bin_idxs.sort(key=lambda b: bin_key(bins[b]))

    capacities = bins[:]

    mapping = [None] * len(items)

    for b in bin_idxs:
        i = 0
        while i < len(item_idxs):
            try:
                i = next(i for i in range(i, len(item_idxs)) 
                         if items[item_idxs[i]] <= capacities[b])
                j = item_idxs[i]
                mapping[j] = b
                capacities[b] -= items[j]
                del item_idxs[i]
            except StopIteration:
                i += 1

    if len(item_idxs) > 0:
        return None

    return mapping

def pack_select_by_items(items=None, bins=None, item_key=None, match_key=None):

    item_idxs = range(len(items))
    bin_idxs = range(len(bins))

    if item_key:
        items_idxs.sort(key=lambda i: item_key(items[i]))

    capacities = bins[:]

    mapping = [None] * len(items)

    for i in item_idxs:
        try:
            b = max((b for b in bin_idxs if items[i] <= capacities[b]), 
                    key=lambda b: match_key(items[i], capacities[b]))
            mapping[i] = b
            capacities[b] -= items[i]
        except ValueError:
            return None

    return mapping

def pack_select_by_bins(items=None, bins=None, bin_key=None, match_key=None):

    item_idxs = range(len(items))
    bin_idxs = range(len(bins))

    if bin_key:
        bin_idxs.sort(key=lambda b: bin_key(bins[b]))

    mapping = [None] * len(items)

    for b in bin_idxs:
        i = 0
        while i < len(item_idxs):
            try:
                i = max((i for i in range(i, len(item_idxs)) 
                        if items[item_idxs[i]] <= capacities[b]),
                        key=lambda i: match_key(items[item_idxs[i]], capacities[b]))
                j = item_idxs[i]
                mapping[j] = b
                capacities[b] -= items[j]
                del item_idxs[i]
            except ValueError:
                i += 1

    if len(item_idxs) > 0:
        return None

    return mapping
