import os


def read_patterns(pattern_file, with_intent=False):
    """
    Reads the pattern files from the pattern file
    :param pattern_file: str, path of the pattern file containing the pattern files and their intent (if needed)
    :param with_intent: boolean, whether or not there are intents in front of the pattern files
    :return: dictionary {intent:patterns} with '1' for intent if with_intent is false
    """
    f = open(pattern_file, 'r')
    lines = f.readlines()
    f.close()
    patterns = {}
    if not with_intent:
        patterns['1'] = []
    for l in lines:
        if with_intent:
            ls = l.strip().split()
            f = open(os.path.join(os.path.dirname(pattern_file), ls[1]), 'r')
            if ls[0] in patterns:
                patterns[ls[0]].extend(f.readlines())
            else:
                patterns[ls[0]] = f.readlines()
            f.close()
        else:
            f = open(os.path.join(os.path.dirname(pattern_file), l.strip()), 'r')
            patterns['1'].extend(f.readlines())
            f.close()
    return patterns


def read_mentions(list_path):
    f = open(list_path, 'r')
    lines = f.readlines()
    f.close()
    mentions = {}
    for l in lines:
        ls = l.strip().split()
        f = open(os.path.join(os.path.dirname(list_path), ls[1]), 'r')
        mentions[ls[0]] = [l.strip() for l in f if l != '' or l != '\n']
        f.close()
    return mentions

def write_patterns(patterns, pattern_path, patterns_dir, with_intent=False):
    """

    :param patterns:
    :param pattern_path:
    :param patterns_dir:
    :param with_intent:
    :return:
    """
    if not os.path.exists(patterns_dir):
        os.mkdir(patterns_dir)

    f = open(pattern_path, 'w')
    if not with_intent:
        f.write(f'{patterns_dir}/patterns.txt\n')
        pat = open(f'{patterns_dir}/patterns.txt', 'w')
        pat.writelines(patterns['1'])
        pat.close()
    if with_intent:
        for i, pats in patterns.items():
            f.write(f'{i} {patterns_dir}/patterns_{i}.txt\n')
            pat = open(f'{patterns_dir}/patterns_{i}.txt', 'w')
            pat.writelines(patterns[i])
            pat.close()
    f.close()


def write_mentions(mentions, mention_path, mentions_dir):
    """

    :param mentions:
    :param mention_path:
    :param mentions_dir:
    :return:
    """
    if not os.path.exists(mentions_dir):
        os.mkdir(mentions_dir)

    f = open(mention_path, 'w')
    for i, ments in mentions.items():
        f.write(f'{i} {mentions_dir}/{i}.lst\n')
        pat = open(f'{mentions_dir}/{i}.lst', 'w')
        pat.writelines(ments)
        pat.close()
    f.close()
