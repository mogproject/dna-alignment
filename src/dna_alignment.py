#!/usr/bin/env python3
from __future__ import division, print_function, absolute_import, unicode_literals

#
# Usage:
#     dna_alignment.py <file_path>
#       (the first line will be considered as a standard sequence)
#     dna_alignment.py test
#

import sys
import fileinput


MAX_SEQUENCE_LENGTH = 150
PADDING_CHAR = '-'


def find_largest_common_sequence(a, b):
    """
    Find the largest continuous common sequence.
    If there are more than one largest sequences, returns the first one.

    :param a: <sequence#1> (string)
    :param b: <sequence#2> (string)
    :return: tuple of (length of the common sequence, position in 'a', position in 'b')
    """
    n = len(a)
    m = len(b)

    msg = 'length of %s must be between 0 and %d (actual=%d)'
    assert 0 <= n <= MAX_SEQUENCE_LENGTH, msg % ('a', MAX_SEQUENCE_LENGTH, n)
    assert 0 <= m <= MAX_SEQUENCE_LENGTH, msg % ('b', MAX_SEQUENCE_LENGTH, m)

    # initialize
    memo = [[0] * (n + 1) for _ in range(m + 1)]

    # fill matrix
    max_common_len = 0
    start_pos_i = 0
    start_pos_j = 0

    for i in range(m):
        for j in range(n):
            common_len = (memo[i][j] + 1) if a[j] == b[i] else 0
            if max_common_len < common_len:
                max_common_len = common_len
                start_pos_i = i - max_common_len + 1
                start_pos_j = j - max_common_len + 1
            memo[i + 1][j + 1] = common_len

    return max_common_len, start_pos_j, start_pos_i


def align_sequence(standard, seq):
    """
    Align a sequence based on the standard string. The result is padded with '-'

    :param standard: (string)
    :param seq: <sequence#2> (string)
    :return: aligned seq (string)
    """

    # examine the entire sequence
    c, a, b = find_largest_common_sequence(standard, seq)
    if c == 0:
        return seq

    # examine the former part
    xa = standard[0:a]
    xb = seq[0:b]
    cx, ax, bx = find_largest_common_sequence(xa, xb)

    # examine the latter part
    ya = standard[a + c:]
    yb = seq[b + c:]
    cy, ay, by = find_largest_common_sequence(ya, yb)

    # print('DEBUG: cx=%d, ax=%d, bx=%d, c=%d, a=%d, b=%d, cy=%d, ay=%d, by=%d' % (cx, ax, bx, c, a, b, cy, ay, by))

    # padding
    buf = []
    if cx < cy:
        ax, bx, cx, a, b, c = a, b, c, a + c + ay, b + c + by, cy

    buf.append(seq[:bx])
    buf.append(PADDING_CHAR * (ax - bx))
    buf.append(seq[bx:b])
    buf.append(PADDING_CHAR * (a - b - max(0, ax - bx)))
    buf.append(seq[b:])

    return ''.join(buf)


def test():
    """
    Unit testing
    """

    def f(func, data):
        for d in data:
            sys.stdout.write('.')
            actual = func(*d[0])
            expected = d[1]
            assert actual == expected, 'param: %s, actual: %s, expected: %s' % (d[0], actual, expected)

    data_1 = [
        [('AAGTTT', 'AACTTT'), (3, 3, 3)],
        [('AAGTTT', 'AATTTC'), (3, 3, 2)],
        [('AAGTTT', 'AACCTT'), (2, 0, 0)],
        [('AAGTTT', 'CAATTT'), (3, 3, 3)],
        [('AAGTTT', 'AATTGG'), (2, 0, 0)],
        [('AAGTTT', 'AGTTTA'), (5, 1, 0)],

        [('', ''), (0, 0, 0)],
        [('', 'A'), (0, 0, 0)],
        [('A', ''), (0, 0, 0)],
        [('A', 'A'), (1, 0, 0)],
        [('A', 'G'), (0, 0, 0)],
        [('A', 'GA'), (1, 0, 1)],
        [('A', 'AG'), (1, 0, 0)],
        [('GA', 'A'), (1, 1, 0)],
        [('AG', 'A'), (1, 0, 0)],
        [('AAAGGG', 'AAG'), (3, 1, 0)],
        [('AAAGGG', 'GA'), (1, 3, 0)],
        [('AAACGGG', 'AG'), (1, 0, 0)],
        [('GAATTCAGTTA', 'GGATCGA'), (2, 0, 1)],
        [('GATCACTAGCAGCAGT', 'GACTAGGAGTACACCC'), (5, 4, 1)],
        [('GATCACTAGCAGCAGT', 'GATCACTAGCAGCAGT'), (16, 0, 0)],
        [('GATCACTATTTTTTTT', 'GTTTTTTTGATCACTA'), (8, 0, 8)],
        [('GATCACTATTTTTTTT', 'TTTTTTTTGATCACTA'), (8, 8, 0)],
    ]

    data_2 = [
        [('AAGTTT', 'AACTTT'), 'AACTTT'],
        [('AAGTTT', 'AATTTC'), 'AA-TTTC'],
        [('AAGTTT', 'AACCTT'), 'AACCTT'],
        [('AAGTTT', 'CAATTT'), 'CAATTT'],
        [('AAGTTT', 'AATTGG'), 'AA-TTGG'],
        [('AAGTTT', 'AGTTTA'), '-AGTTTA'],

        [('A', 'A'), 'A'],
        [('A', 'G'), 'G'],
        [('A', 'GA'), 'GA'],
        [('A', 'AG'), 'AG'],
        [('GA', 'A'), '-A'],
        [('AG', 'A'), 'A'],
        [('AAAGGG', 'AAG'), '-AAG'],
        [('AAAGGG', 'GA'), '---GA'],
        [('AAACGGG', 'AG'), 'A---G'],
        [('GAATTCAGTTA', 'GGATCGA'), 'GGA-TCGA'],
        [('GATCACTAGCAGCAGT', 'GACTAGGAGTACACCC'), 'G---ACTAGG---AGTACACCC'],
        [('GATCACTAGCAGCAGT', 'GATCACTAGCAGCAGT'), 'GATCACTAGCAGCAGT'],
        [('GATCACTATTTTTTTT', 'GTTTTTTTGATCACTA'), 'GTTTTTTTGATCACTA'],
        [('GATCACTATTTTTTTT', 'TTTTTTTTGATCACTA'), '--------TTTTTTTTGATCACTA'],
    ]

    f(find_largest_common_sequence, data_1)
    f(align_sequence, data_2)

    print('\nok')


def main(args):
    """
    Main function

    :param args: command-line arguments
    :return: exit code
    """

    standard = ''
    for line in fileinput.input(args):
        line = line.rstrip()
        if not standard:
            standard = line
            print(standard)
        else:
            print(align_sequence(standard, line))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['test']:
        test()
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))

