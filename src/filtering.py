import os, sys


#path = os.path.dirname(__file__)
#sys.path.append(path + '/../model')
#sys.path.append(path + '/../algos')
#sys.path.append(path + '/../extractions')
#sys.path.append(path + '/../methods')
#sys.path.append(path + '/../utils')


def filter_patterns(patterns, min_token, max_token, min_slot, max_slot):
    """

    :param patterns:
    :param min_token:
    :param max_token:
    :param min_slot:
    :param max_slot:
    :return:
    """
    filtered = {}
    for i, pats in patterns.items():
        filtered[i] = []
        for p in pats:
            toks = len(p.split())
            slots = p.count('$')
            if toks > max_token or toks < min_token:
                continue
            if slots > max_slot or slots < min_slot:
                continue
            filtered[i].append(p)

    return filtered


def filter_mentions(mentions, min_token, max_token):
    """

    :param mentions:
    :param min_token:
    :param max_token:
    :return:
    """
    filtered = {}
    for i, ments in mentions.items():
        filtered[i] = []
        for m in ments:
            toks = len(m.split())
            if toks > max_token or toks < min_token:
                continue
            filtered[i].append(f'{m}\n')
    return filtered


