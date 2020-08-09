import sys

print("Result is", sys.argv[1:])
#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
from textwrap import dedent
from itertools import zip_longest


def process_chunk(data):
    """Replace this with your own function
    that processes data one line at a
    time"""

    print("data", data)
    data = data.strip() + ' processed'
    return data


def grouper(line_cnt, iterable, padvalue=None):
    """grouper(3, 'abcdefg', 'x') -->
    ('a','b','c'), ('d','e','f'), ('g','x','x')"""

    print("line_cnt", line_cnt)
    return zip_longest(*[iter(iterable)]*line_cnt, fillvalue=padvalue)


if __name__ == '__main__':

    # test data
    test_data = """\
	1 some test garbage
	2 some test garbage
	3 some test garbage
	4 some test garbage
	5 some test garbage
	6 some test garbage
	7 some test garbage
	8 some test garbage
	9 some test garbage
	10 some test garbage
	11 some test garbage
	12 some test garbage
	13 some test garbage
	14 some test garbage
	15 some test garbage
	16 some test garbage
	17 some test garbage
	18 some test garbage
	19 some test garbage
	20 some test garbage"""
    test_data = dedent(test_data)
    test_data = test_data.split("\n")

    # Create pool (p)
    p = multiprocessing.Pool(4)

    # Use 'grouper' to split test data into
    # groups you can process without using a
    # ton of RAM. You'll probably want to
    # increase the chunk size considerably
    # to something like 1000 lines per core.

    # The idea is that you replace 'test_data'
    # with a file-handle
    # e.g., testdata = open(file.txt,'rU')

    # And, you'd write to a file instead of
    # printing to the stout

    # chunk to be increased to 1000
    for chunk in grouper(10, test_data):
        print("chunk", chunk)
        results = p.map(process_chunk, chunk)
        for r in results:
            print(r) 	# replace with outfile.write()
