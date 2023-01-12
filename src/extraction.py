import sys
import os
import re

#path = os.path.dirname(__file__)
#sys.path.append(path + '/../model')
#sys.path.append(path + '/../algos')
#sys.path.append(path + '/../extractions')
#sys.path.append(path + '/../methods')
#sys.path.append(path + '/../utils')

import numpy as np
import matplotlib.pyplot as plt
import random


def split_line(line):
    '''
    Splits a line in a triplet being the list of the words from the first half of the line, the list of the words
    from the second half of the line -1 and the last word which represent :
        - the list of the words from the sentence containing the tags BOS and EOS,
        - the list of the labels associated,
        - the tag of the sentence
    :param line: output of readline
    :return: a list
    '''
    l = line.split()
    sentence, labels, intent = l[:len(l)//2], l[len(l)//2:-1], l[-1]
    return [sentence, labels, intent]


def read_w_intent(path, length):
    '''
    Reads every line from path using split_line()
    :param path: string, path of the file you want to open
    :return: the list of every output from split_line
    '''
    f = open(path, 'r')
    r = []
    for l in f.readlines()[:length]:
        r.append(split_line(l))
    f.close()
    return r


def read_w_intent2(path, beg, end):
    '''
    Reads every line from path using split_line()
   :param path: string, path of the file you want to open
   :return: the list of every output from split_line
    '''
    f = open(path, 'r')
    r = []
    for l in f.readlines()[beg:end]:
        r.append(split_line(l))
    f.close()
    return r

"""
def process_sentence(sentence, tags, vocab, null, pad, front_label=True):
    '''
    Process a line from read and split with read_w_intent
    :param sentence: list of strings
    :param tags: list of strings
    :param vocab: dictionnary
    :return: string
    '''
    pattern = ''
    stag = []
    t = ''
    s = ''
    mentions = []
    for i in range(pad, len(sentence) - pad):
        if tags[i] != null:
            if t == '':
                s = sentence[i]
                if front_label:
                    t = tags[i][2:]
                else:
                    t = tags[i][:-2]
            elif (front_label and t != tags[i][2:]) or (not front_label and t != tags[i][:-2]):
                if t not in vocab:
                    vocab[t] = {s}
                    mentions.append(s)
                else:
                    vocab[t].add(s)
                    mentions.append(s)
                if front_label:
                    t = tags[i][2:]
                else:
                    t = tags[i][:-2]
                s = sentence[i]
            else:
                s += f' {sentence[i]}'
        elif t != '' and s != '':
            if t not in vocab:
                vocab[t] = {s}
                mentions.append(s)
            else:
                vocab[t].add(s)
                mentions.append(s)
            pattern += f' ${t} {sentence[i]}'
            stag.append(t)
            t, s = '', ''
        else:
            pattern += f' {sentence[i]}'
            t, s = '', ''
    if t != '' and s != '':
        if t not in vocab:
            vocab[t] = {s}
            mentions.append(s)
        else:
            vocab[t].add(s)
            mentions.append(s)
        pattern += f' ${t}'
        stag.append(t)
    return pattern[1:], stag, mentions
"""

def process_sentence(sentence, tags, vocab, null, pad, front_label=True):
    '''
    Process a line from read and split with read_w_intent
    :param sentence: list of strings
    :param tags: list of strings
    :param vocab: dictionnary
    :return: string
    '''
    pattern = ''
    stag = []
    t = ''
    s = ''
    mentions = []
    for i in range(pad, len(sentence) - pad):
        if tags[i] != null:
            if (tags[i][0] == 'B' and front_label) or (tags[i][-1] == 'B' and not front_label):
                if t != '':
                    if t in vocab:
                        vocab[t].add(s)
                    else:
                        vocab[t] = {s}
                    mentions.append(s)
                    pattern += f' ${t}'
                    stag.append(t)
                t = (tags[i][2:] if front_label else tags[i][:-2])
                s = sentence[i]
            else:
                s += f' {sentence[i]}'
        else:
            if t != '':
                if t in vocab:
                    vocab[t].add(s)
                else:
                    vocab[t] = {s}
                mentions.append(s)
                pattern += f' ${t}'
                stag.append(t)
                t = ''
                s = ''
            pattern += f' {sentence[i]}'

    if t != '':
        if t in vocab:
            vocab[t].add(s)
        else:
            vocab[t] = {s}
        mentions.append(s)
        pattern += f' ${t}'
        stag.append(t)

    return pattern[1:], stag, mentions

def process_sentence2(sentence, tags, vocab, null, pad, front_label=True):
    '''
    Process a line from read and split with read_w_intent
    :param sentence: list of strings
    :param tags: list of strings
    :param vocab: dictionnary
    :return: string
    '''
    pattern = ''
    stag = []
    t = ''
    s = ''
    mentions = []
    for i in range(pad, len(sentence) - pad):
        if tags[i] != null:
            if (tags[i][0] == 'B' and front_label) or (tags[i][-1] == 'B' and not front_label):
                if t != '':
                    if t in vocab:
                        vocab[t].append(s)
                    else:
                        vocab[t] = [s]
                    mentions.append(s)
                    pattern += f' ${t}'
                    stag.append(t)
                t = (tags[i][2:] if front_label else tags[i][:-2])
                s = sentence[i]
            else:
                s += f' {sentence[i]}'
        else:
            if t != '':
                if t in vocab:
                    vocab[t].append(s)
                else:
                    vocab[t] = [s]
                mentions.append(s)
                pattern += f' ${t}'
                stag.append(t)
                t = ''
                s = ''
            pattern += f' {sentence[i]}'

    if t != '':
        if t in vocab:
            vocab[t].append(s)
        else:
            vocab[t] = [s]
        mentions.append(s)
        pattern += f' ${t}'
        stag.append(t)

    return pattern[1:], stag, mentions


def mk_vocab_patterns(read_doc, null='O', pad=1, front_label=True):
    '''
    Applies process_sentence to each line of the output of read_w_intent
    :param read_doc: output of read_w_intent
    :return: a dictionnary like :
        { tag 1 : { expression 1, expression 2, ..., expression n1 },
                ... ,
        tag k : { expression 1, expression 2, ..., expression nk } }
        and a list of strings containing the patterns
    '''
    v = {}
    patterns = {}
    for i in range(len(read_doc)):
        p, s, _ = process_sentence(read_doc[i][0], read_doc[i][1], v, null, pad, front_label=front_label)
        #if len(s) == 0:
            #print(read_doc[i])
        if p in patterns:
            patterns[p][1].add(read_doc[i][2])
        else:
            patterns[p] = [s, {read_doc[i][2]}]

    return v, patterns


def mk_vocab_patterns_list(read_doc, null='O', pad=1, front_label=True, un=False):
    '''
    Applies process_sentence to each line of the output of read_w_intent
    :param read_doc: output of read_w_intent
    :return: a dictionnary like :
        { tag 1 : { expression 1, expression 2, ..., expression n1 },
                ... ,
        tag k : { expression 1, expression 2, ..., expression nk } }
        and a list of strings containing the patterns
    '''
    v = {}
    patterns = []
    for i in range(len(read_doc)):
        p, s, _ = process_sentence(read_doc[i][0], read_doc[i][1], v, null, pad, front_label=front_label)
        #if len(s) == 0:
            #print(read_doc[i])
        if un:
            if patterns.count(p) == 0:
                patterns.append(p)
        else:
            patterns.append(p)
    return v, patterns

def mk_vocab_list_patterns(read_doc, null='O', pad=1, front_label=True):
    '''
        Applies process_sentence to each line of the output of read_w_intent
        :param read_doc: output of read_w_intent
        :return: a dictionnary like :
            { tag 1 : [ expression 1, expression 2, ..., expression n1 ],
                    ... ,
            tag k : [ expression 1, expression 2, ..., expression nk ] }
            and a list of strings containing the patterns
        '''
    v = {}
    patterns = {}
    for i in range(len(read_doc)):
        p, s, _ = process_sentence2(read_doc[i][0], read_doc[i][1], v, null, pad, front_label=front_label)
        # if len(s) == 0:
        # print(read_doc[i])
        if p in patterns:
            patterns[p][1].add(read_doc[i][2])
        else:
            patterns[p] = [s, {read_doc[i][2]}]

    return v, patterns

def mk_vocab_list_patterns_list(read_doc, null='O', pad=1, front_label=True, un=False):
    '''
    Applies process_sentence to each line of the output of read_w_intent
    :param read_doc: output of read_w_intent
    :return: a dictionnary like :
        { tag 1 : { expression 1, expression 2, ..., expression n1 },
                ... ,
        tag k : { expression 1, expression 2, ..., expression nk } }
        and a list of strings containing the patterns
    '''
    v = {}
    patterns = []
    for i in range(len(read_doc)):
        p, s, _ = process_sentence2(read_doc[i][0], read_doc[i][1], v, null, pad, front_label=front_label)
        #if len(s) == 0:
            #print(read_doc[i])
        if un:
            if patterns.count(p) == 0:
                patterns.append(p)
        else:
            patterns.append(p)
    return v, patterns

def write_patterns_list(path, ver, patterns):
    '''
    Writes the patterns files of form intent_with_categories.txt
    :param patterns:
    :return:
    '''
    if not os.path.exists(f'{path}patterns{ver}'):
        os.mkdir(f'{path}patterns{ver}')

    f = open(f'{path}patterns{ver}/patterns.txt', 'w')
    pat = open(f'{path}patterns_{ver}.txt', 'w')
    for s in patterns:
        f.write(f'{s}\n')
    f.close()
    pat.write(f'patterns{ver}/patterns.txt\n')
    pat.close()




def fill(patterns, p, m, n, i, indexes):
    """
    Fills the patterns with the
    :param patterns: list
    :param p: list of strings: pattern to fill
    :param m: list of strings: mentions
    :param n: int: number or slots to fill
    :param i: int: from which point slots need to be filled
    :param indexes: list of int : list of indexes
    :return:
    """
    if n == 0:
        s = ''
        for w in p:
            s += f' {w}'
        patterns.append(s[1:])
    else:
        for j in range(i, len(m)):
            ps = p.copy()
            ps[indexes[j]] = f'<{p[indexes[j]][1:]}> {m[j]} <\\{p[indexes[j]][1:]}>'
            fill(patterns, ps, m, n-1, j+1, indexes)



def mk_vocab_patterns2(read_doc, max_slots, null='O', pad=1, front_label=True):
    '''
    Applies process_sentence to each line of the output of read_w_intent
    :param read_doc: output of read_w_intent
    :return: a dictionnary like :
        { tag 1 : { expression 1, expression 2, ..., expression n1 },
                ... ,
        tag k : { expression 1, expression 2, ..., expression nk } }
        and a list of strings containing the patterns
    '''
    v = {}
    patterns = {}
    for i in range(len(read_doc)):
        p, _, m = process_sentence(read_doc[i][0], read_doc[i][1], v, null, pad, front_label=front_label)
        n = len(m) - max_slots
        ps = p.split()
        indexes = [j for j in range(len(ps)) if ps[j][0] == '$']
        pats = []
        fill(pats, ps, m, n, 0, indexes)
        for pa in pats:
            if pa in patterns:
                patterns[pa][1].add(read_doc[i][2])
            else:
                patterns[pa] = [re.findall('[ \^]\$([a-zA-Z0-9\-\_\.]*)[ \$\#]?', pa), {read_doc[i][2]}] #Potentiellement mauvaise regex
    return v, patterns


def save_lists(path, ver, voc):
    '''
    saves vocabulary for each class
    :param voc: output of mk_vocab
    :return: nothing
    '''
    if not os.path.exists(f'{path}_{ver}'):
        os.mkdir(f'{path}_{ver}')
    for k, v in voc.items():
        f = open(f'{path}_{ver}/{k}.lst', 'w')
        b = []
        for e in v:
            b.append(f'{e}\n')
        f.writelines(b)
        f.close()



def save_lists2(path, ver, voc):
    '''
    saves vocabulary for each class
    :param voc: output of mk_vocab
    :return: nothing
    '''
    if not os.path.exists(f'{path}_{ver}'):
        os.mkdir(f'{path}_{ver}')
    for k, v in voc.items():
        f = open(f'{path}_{ver}/{k}.lst', 'w')
        b = []
        for e in list(v)[:(len(v)//2)+1]:
            b.append(f'{e}\n')
        f.writelines(b)
        f.close()




def save_classes(path, ver, voc):
    '''
    saves the couples of classes and their vocab file in a classes.txt file at cwd
    :param voc: output of mk_vocab
    :return: nothing
    '''
    f = open(f'{path}lists_{ver}.txt', 'w')
    s = ''
    for k, _ in voc.items():
        s += f'{k} lists_{ver}/{k}.lst\n'
    f.write(s)
    f.close()



"""
def mk_pat_p_pat(path, ver, patterns, short=4, max_l=6):
    '''
    Writes the patterns files of form intent_with_categories.txt
    :param patterns:
    :return:
    '''
    files = {}
    i = 0
    for s, l in patterns.items():
        if len(l[0]) >= max_l:
            continue
        if len(l[0]) >= short:
            fname = f'{i}_with_many.txt'
        else:
            fname = f'{i}.txt'
        files[fname] = f'{s}\n'
        i+=1

    if not os.path.exists(f'{path}patterns{ver}'):
        os.mkdir(f'{path}patterns{ver}')

    pat = open(f'{path}patterns_{ver}.txt', 'w')
    pat_short = open(f'{path}patterns_{ver}_short.txt', 'w')

    for k, v in files.items():
        f = open(f'{path}patterns{ver}/{k}', 'w')
        f.write(f'{v}')
        f.close()
        if k[-8:-4] == 'many':
            pat_short.write(f'patterns{ver}/{k}\n')
        else:
            pat.write(f'patterns{ver}/{k}\n')
    pat.close()
    pat_short.close()
"""


def mk_pat_p_pat(path, ver, patterns):
    '''
    Writes the patterns files of form intent_with_categories.txt
    :param patterns:
    :return:
    '''
    files = {}
    i = 0
    for s, l in patterns.items():
        fname = f'{i}.txt'
        files[fname] = f'{s}\n'
        i+=1

    if not os.path.exists(f'{path}patterns{ver}'):
        os.mkdir(f'{path}patterns{ver}')

    pat = open(f'{path}patterns_{ver}.txt', 'w')

    for k, v in files.items():
        f = open(f'{path}patterns{ver}/{k}', 'w')
        f.write(f'{v}')
        f.close()
        pat.write(f'patterns{ver}/{k}\n')
    pat.close()


def write_patterns(path, ver, patterns):
    '''
    Writes the patterns files of form intent_with_categories.txt
    :param patterns:
    :return:
    '''
    if not os.path.exists(f'{path}patterns{ver}'):
        os.mkdir(f'{path}patterns{ver}')

    f = open(f'{path}patterns{ver}/patterns.txt', 'w')
    pat = open(f'{path}patterns_{ver}.txt', 'w')
    for s, l in patterns.items():
        f.write(f'{s}\n')
    f.close()
    pat.write(f'patterns{ver}/patterns.txt\n')
    pat.close()


def write_patterns_w_intent(path, ver, patterns):
    if not os.path.exists(f'{path}patterns{ver}'):
        os.mkdir(f'{path}patterns{ver}')

    intents = {}

    for s, l in patterns.items():
        for i in l[1]:
            if i in intents:
                intents[i].append(s)
            else:
                intents[i] = [s]

    f = open(f'{path}patterns_{ver}_w_intent.txt', 'w')
    for i, pats in intents.items():
        inten = open(f'{path}patterns{ver}/patterns_{i}.txt', 'w')
        for p in pats:
            inten.write(f'{p}\n')
        inten.close()
        f.write(f'{i} {path}patterns{ver}/patterns_{i}.txt\n')
    f.close()



def mk_intent_w_categories(path, ver, patterns, short=4, max_l=6, with_intent=True):
    '''
    Writes the patterns files of form intent_with_categories.txt
    :param patterns:
    :return:
    '''
    files = {}

    for s, l in patterns.items():
        if len(l[0]) >= max_l:
            continue
        if with_intent:
            l1 = list(l[1])
            for intent in l1:
                if len(l[0]) >= short:
                    fname = f'{intent}_with_many.txt'
                else:
                    fname = f'{intent}.txt'
                if fname in files:
                    files[fname][0] += f'{s}\n'
                else:
                    files[fname] = [f'{s}\n', intent]
        else:
            fname=''
            if len(l[0]) >= short:
                fname = 'many#'
            elif len(l[0]) == 0:
                fname = 'none#'
            else:
                for tag in l[0]:
                    fname += f'{tag}#'
            fname = fname[:-1]+'.txt'
            if fname in files:
                files[fname][0] += f'{s}\n'
            else:
                files[fname] = [f'{s}\n', fname[:-4]]

    if not os.path.exists(f'{path}patterns{ver}'):
        os.mkdir(f'{path}patterns{ver}')
    pat = open(f'{path}patterns_{ver}.txt', 'w')
    pat_short = open(f'{path}patterns_{ver}_short.txt', 'w')
    for k, v in files.items():
        f = open(f'{path}patterns{ver}/{k}', 'w')
        f.write(v[0])
        f.close()
        if k[-8:-4] == 'many':
            pat_short.write(f'{v[1]} patterns{ver}/{k}\n')
        else:
            pat.write(f'{v[1]} patterns{ver}/{k}\n')
    pat.close()
    pat_short.close()
