import sys
import os
import re

#path = os.path.dirname(__file__)
#sys.path.append(path + '/../model')
#sys.path.append(path + '/../algos')
#sys.path.append(path + '/../extractions')
#sys.path.append(path + '/../methods')
#sys.path.append(path + '/../utils')

from .patterns import read_patterns, read_mentions
#from interface import Generator
import random

slotre = re.compile("\$([-a-zA-Z._0-9]+)")
btre = re.compile("<(.*)>")
etre = re.compile("</(.*)>")
doltre = re.compile("(\$.*)")


class Algo1:

    def __init__(self, pattern_path, list_path, with_intent=False, seed=1):
        self.patterns = read_patterns(pattern_path, with_intent=with_intent)
        self.mentions = read_mentions(list_path)
        self.rand = random.Random()
        self.rand.seed(a=seed)

    def generate(self):
        ...


    def generate_corpus(self, size):
        """

        :param size:
        :return:
        """
        m = 0
        for v in self.patterns.values():
            m += len(v)
        n = size // m + 1
        ns = [n for i in range(m)]
        rm = (n * m) - size
        to_rm = self.rand.sample(range(m), k=rm)
        for i in to_rm:
            ns[i] += -1
        generated = []
        i = 0
        for k, v in self.patterns.items():
            for j in range(len(v)):
                generated.extend(generate_pattern(self.mentions, v[j], ns[i], self.rand, intent=k))
                i += 1
        return generated


def split_pattern(pattern, intent='1'):
    pattern = pattern.split()
    pat = "BOS"
    tags = "O"
    tag = ""
    bi = ""
    for w in pattern:
        bt = re.match(btre, w)
        et = re.match(etre, w)
        dolt = re.match(doltre, w)
        if dolt:
            pat += f" {w}"
            tags += f" {w}"
        elif et:
            tag = ""
            bi = ""
        elif bt:
            tag = bt[1]
            bi = "B"
        else:
            if tag == "":
                pat += f" {w}"
                tags += f" O"
            else:
                pat += f" {w}"
                tags += f" {bi}-{tag}"
                bi = "I"

    pat += f" EOS"
    tags += f" {intent}"
    return pat, tags


def fill_pattern(pattern, tags, fillers):
    pat = pattern
    tag = tags
    for m in fillers:
        t = re.search(slotre, pat)[1]
        n = len(m.split())
        ta = f"B-{t}"
        for i in range(n-1):
            ta += f" I-{t}"
        pat = re.sub(f"\${t}", m, pat, count=1)
        tag = re.sub(f"\${t}", ta, tag, count=1)
    return f"{pat}\t{tag}\n"


def samples(mentions, slots, n, rand):
    combine = 1
    for slot in slots:
        combine = combine * len(mentions[slot])
    if n < combine:
        if combine > (2**63-1):
            to_generate = set()
            while len(to_generate) < n:
                to_generate.add(rand.randrange(combine))
            to_generate = list(to_generate)
        else:
            to_generate = rand.sample(range(combine), k=n)
    else:
        n_full = n // combine
        to_generate = rand.sample(range(combine), k=(n % combine))
        for i in range(n_full):
            to_generate.extend(list(range(combine)))
    return to_generate


def generate_pattern(mentions, pattern, n, rand, intent='1'):
    pat, tags = split_pattern(pattern, intent=intent)
    slots = re.findall(slotre, pat)
    to_generate = samples(mentions, slots, n, rand)
    generated = []
    for i in to_generate:
        fillers = []
        index = i
        for s in slots:
            fillers.append(mentions[s][index%(len(mentions[s]))])
            index = index // (len(mentions[s]))
        generated.append(fill_pattern(pat, tags, fillers))
    return generated


