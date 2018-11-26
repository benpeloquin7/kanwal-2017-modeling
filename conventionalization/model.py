from collections import Counter, defaultdict
import numpy as np

from matrix import *


class Agent:
    """Speaker / listener agent


    Parameters
    ----------
    id: int
        UID for agent.
    input_data: collections.Counter
        {<u_1, m_1> -> cnt, ..., <u_n, m_n> -> cnt}
    alpha: int
        Rationality parameter.
    depth: int
        Recursive depth.

    """

    def __init__(self, id_, input_data, alpha=1, depth=1):
        self.id = id_
        self.id = id_
        self.input_data = input_data
        self.alpha = alpha
        self.depth = depth

    def construct_meaning_prior(self):
        pass

    def construct_utterance_prior(self):
        pass

    def sample(self, k):
        pass


if __name__ == '__main__':

    data = [('zop', 'zopudon'), ('zop', 'zopudon'), ('zopudon', 'zopudon'),
            ('zopudon', 'zopudon'), ('zop', 'zopekil'), ('zopekil', 'zopekil')]
    corpus = Counter(data)


    utterance_cnts = defaultdict(lambda:0)
    meaning_cnts = defaultdict(lambda:0)
    for tup, cnt in corpus.items():
        utterance_cnts[tup[0]] += cnt
        meaning_cnts[tup[1]] += cnt

    cnts = np.array([cnt for u, cnt in utterance_cnts.items()]).astype(float)
    utterances = np.array([u for u, cnt in utterance_cnts.items()])
    p_utterances = np.array([0.7, 0.15, 0.15])

    cnts = np.array([cnt for m, cnt in meaning_cnts.items()]).astype(float)
    meanings = np.array([m for m, cnt in meaning_cnts.items()])
    p_meanings = np.array([0.7, 0.15, 0.15])

    m = idxs2matrix([0, 1, 4, 8], 3, 3)
    print(m)
    for k in range(1, 100):
        print(speaker(m, p_utterances, p_meanings, alpha=1, k=k))

    # print(utterances)
    # print(p_utterances)
    # print(meanings)
    # print(p_meanings)


