#!/usr/bin/python
from __future__ import division, print_function, absolute_import, unicode_literals

import sys


MAX_SEQUENCE_LENGTH = 150
PADDING_CHAR = '_'


def align_sequences(a, b):
    """
    Align two sequences. Results are padded with '_'

    :param a: <sequence#1> (string)
    :param b: <sequence#2> (string)
    :return: tuple of (aligned sequence#1 (string), aligned sequence#2 (string))
    """
    m = len(a)
    n = len(b)

    assert 1 <= m <= MAX_SEQUENCE_LENGTH, 'length of a must be between 1 and %d (actual=%d)' % (MAX_SEQUENCE_LENGTH, m)
    assert 1 <= n <= MAX_SEQUENCE_LENGTH, 'length of b must be between 1 and %d (actual=%d)' % (MAX_SEQUENCE_LENGTH, n)

    # initialize
    memo = [[0] * (m + 1) for _ in range(n + 1)]

    # fill matrix
    for i in range(n):
        for j in range(m):
            s = 1 if a[j] == b[i] else 0
            memo[i + 1][j + 1] = max(memo[i][j] + s, memo[i + 1][j], memo[i][j + 1])

    # traceback
    buf_a = []
    buf_b = []

    i = n
    j = m
    while 0 < i or 0 < j:
        if 0 < i and 0 < j and a[j - 1] == b[i - 1]:
            i -= 1
            j -= 1
            buf_a.append(a[j])
            buf_b.append(b[i])
        elif 0 < j and memo[i][j - 1] == memo[i][j]:
            j -= 1
            buf_a.append(a[j])
            buf_b.append(PADDING_CHAR)
        elif 0 < i and memo[i - 1][j] == memo[i][j]:
            i -= 1
            buf_a.append(PADDING_CHAR)
            buf_b.append(b[i])
        else:
            raise Exception('never happens')

    ret_a = ''.join(reversed(buf_a))
    ret_b = ''.join(reversed(buf_b))
    return ret_a, ret_b


def test():
    """
    Unit testing
    """
    data = [
        ('A', 'A', 'A', 'A'),
        ('A', 'G', '_A', 'G_'),
        ('A', 'GA', '_A', 'GA'),
        ('A', 'AG', 'A_', 'AG'),
        ('GA', 'A', 'GA', '_A'),
        ('AG', 'A', 'AG', 'A_'),
        ('AAAGGG', 'AAG', 'AAAGGG', '_AA__G'),
        ('AAAGGG', 'GA', '_AAAGGG', 'G__A___'),
        ('AAACGGG', 'AG', 'AAACGGG', '__A___G'),
        ('GAATTCAGTTA', 'GGATCGA', '_GAATTCAGTTA', 'GG_A_TC_G__A'),
        ('GATCACTAGCAGCAGT', 'GACTAGGAGTACACCC', 'GATCACTA_GCAG__CA___GT', 'G___ACTAGG_AGTACACCC__'),
    ]

    for d in data:
        sys.stdout.write('.')
        actual = align_sequences(d[0], d[1])
        expected = d[2:]
        assert actual == expected, 'actual: %s, expected: %s' % (actual, expected)
    print('\nok')


def main(args):
    """
    Main function

    :param args: command-line arguments
    :return: exit code
    """
    ret = align_sequences(args[0], args[1])
    print(ret[0])
    print(ret[1])
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['test']:
        test()
        sys.exit(0)
    if len(sys.argv) != 3:
        print('usage: %s <sequence1> <sequence2>' % sys.argv[0])
        print('       %s test' % sys.argv[0])
        sys.exit(1)
    sys.exit(main(sys.argv[1:]))
