from collections import Counter
from datetime import datetime
from importlib import import_module
from os.path import isfile
import time

from .util import verify_mapping

def pack_vectors(problem, **kwargs):

    if problem is None:
        return None

    family = kwargs.get('family', 'stillwell_current')

    module = import_module('.{:s}'.format(family), package='vectorpack') 

    start_time = time.process_time()
    result = module.pack_vectors(problem, **kwargs)
    stop_time = time.process_time()

    mapping = result['mapping']

    return result.update({
        'solver-githash' : '__GITHASH__',
        'problem-argshash' : problem.get('argshash', None),
        'family' : family,
        'datetime' : datetime.now(),
        'failcount' : mapping.count(None),
        'bincount' : len(Counter(mapping)),
        'verified' : verify_mapping(**result),
        'runtime' : stop_time - start_time,
    })


def generate_problem(**kwargs):

    family = kwargs.get('family', 'stillwell_current')

    module = import_module('.{:s}'.format(family), package='vectorpack')

    result = module.generate_problem(**kwargs)

    return result.update({
        'family' : family
    })
