"""matrix.py

Define all RSA behaviors via matrix operations.

"""

import numpy as np


def idxs2matrix(idxs, m, n):
    """Convert a list of indices to an M x N matrix.

    Example
    -------
    m, n = 3, 3
    idxs = [0, 2, 3, 8]

    idxs2matrix(idxs, m, n) -->

            [[1., 0., 1.],
             [1., 0., 0.],
             [0., 0., 1.]]

    """
    d = []
    for row in range(m):
        curr_row = []
        for col in range(n):
            if (row * n + col) in idxs:
                curr_row.append(1.)
            else:
                curr_row.append(0.)
        d.append(curr_row)
    return np.array(d)

def is_literal(m):
    pass


def row_normalize(m):
    """All rows sum to 1"""
    totals = np.sum(m, axis=1)
    M = np.nan_to_num((m.transpose() / totals).transpose())
    return M


def col_normalize(m):
    """All cols sum to 1"""
    totals = np.sum(m, axis=0)
    return np.nan_to_num((m / totals))


def row_multiply(m, k):
    assert m.shape[0] == len(k)
    return (m.transpose() * k).transpose()


def col_multiply(m, k):
    assert m.shape[1] == len(k)
    return m * k


def run_listener_forward(M, p_meanings):
    return row_normalize(col_multiply(np.exp(np.log(M)), p_meanings))


def run_speaker_forward(M, p_utterances, alpha=1.):
    return col_normalize(row_multiply(np.exp(alpha * np.log(M)), p_utterances))


def speaker(M, p_utterances, p_meanings, alpha=1., k=1):
    M_ = M
    for _ in range(k):
        M_ = run_listener_forward(M_, p_meanings)
        M_ = run_speaker_forward(M_, p_utterances, alpha)
    return M_


def listener(M, p_utterances, p_meanings, alpha=1., k=0):
    M_ = run_listener_forward(M, p_meanings)
    for _ in range(k):
        M_ = run_speaker_forward(M_, p_utterances, alpha)
        M_ = run_listener_forward(M_, p_meanings)
    return M_