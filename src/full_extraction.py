import sys
import os

import random

#path = os.path.dirname(__file__)
#sys.path.append(path + '/../model')
#sys.path.append(path + '/../algos')
#sys.path.append(path + '/../extractions')
#sys.path.append(path + '/../methods')
#sys.path.append(path + '/../utils')

from .extraction import *

def extract(working_path, file_path, i):
    ver = f'{i}'
    r = read_w_intent(file_path, i)
    v, patterns = mk_vocab_patterns(r)

    save_lists(f'{working_path}/lists', ver, v)
    save_classes(f'{working_path}/', ver, v)

    write_patterns(f'{working_path}/', ver, patterns)


def make_list(working_path, file_path, i):
    ver = f'{i}'
    r = read_w_intent(file_path, i)
    v, patterns = mk_vocab_patterns_list(r)

    save_lists(f'{working_path}/lists', ver, v)
    save_classes(f'{working_path}/', ver, v)

    write_patterns_list(f'{working_path}/', ver, patterns)


def make_var_patterns(working_path, file_path, i):
    ver = f'{i}'
    r = read_w_intent(file_path, None)
    v, patterns = mk_vocab_patterns_list(r, un=True)

    save_lists2(f'{working_path}/lists', ver, v)
    save_classes(f'{working_path}/', ver, v)

    write_patterns_list(f'{working_path}/', ver, patterns[:i])


def extract_with_multiplicity(working_path, file_path, i):
    ver = f'{i}'
    r = read_w_intent(file_path, i)
    v, patterns = mk_vocab_list_patterns(r)

    save_lists(f'{working_path}/lists', ver, v)
    save_classes(f'{working_path}/', ver, v)

    write_patterns(f'{working_path}/', ver, patterns)

def extract_with_all_multiplicity(working_path, file_path, i):
    ver = f'{i}'
    r = read_w_intent(file_path, i)
    v, patterns = mk_vocab_list_patterns_list(r)

    save_lists(f'{working_path}/lists', ver, v)
    save_classes(f'{working_path}/', ver, v)

    write_patterns_list(f'{working_path}/', ver, patterns)

