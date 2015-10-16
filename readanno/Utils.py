__author__ = 'luocheng'


def str2numseq(s,splitter):
    return [int(item) for item in s.strip().split(splitter)]

def numseq2str(numseq,splitter):
    return [splitter.join([str(item) for item in numseq])

