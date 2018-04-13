import pandas as pd
from itertools import islice

df = pd.read_csv('../metadata/metadata.csv')

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        flat_list = [item for sublist in result for item in sublist]
        yield ''.join(flat_list)

list(window(df['characters'][0], len('(Marvel) ')))

if substring == '(Marvel) ':
    'poop'
    # split at end of substring
elif substring == '(Marvel)(':
    'poop'
    # split at end of next closing parens
else:
    pass
