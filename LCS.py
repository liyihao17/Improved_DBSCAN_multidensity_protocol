def lcs_len(a, b):
    '''
    a, b: strings
    '''
    n = len(a)
    m = len(b)
    l = [([0] * (m + 1)) for i in range(n + 1)]
    direct = [([0] * m) for i in range(n)]  # 0 for top left, -1 for left, 1 for top

    for i in range(n + 1)[1:]:
        for j in range(m + 1)[1:]:
            if a[i - 1] == b[j - 1]:
                l[i][j] = l[i - 1][j - 1] + 1
            elif l[i][j - 1] > l[i - 1][j]:
                l[i][j] = l[i][j - 1]
                direct[i - 1][j - 1] = -1
            else:
                l[i][j] = l[i - 1][j]
                direct[i - 1][j - 1] = 1
    return l, direct


def get_lcs(direct, a, i, j):
    '''
    direct: martix of arrows
    a: the string regarded as row
    i: len(a) - 1, for initialization
    j: len(b) - 1, for initialization
    '''
    lcs = []
    get_lcs_inner(direct, a, i, j, lcs)
    return lcs


def get_lcs_inner(direct, a, i, j, lcs):
    if i < 0 or j < 0:
        return
    if direct[i][j] == 0:
        get_lcs_inner(direct, a, i - 1, j - 1, lcs)
        lcs.append(a[i])
    elif direct[i][j] == 1:
        get_lcs_inner(direct, a, i - 1, j, lcs)
    else:
        get_lcs_inner(direct, a, i, j - 1, lcs)

def get_lcs_distance(a,b):
    a_new = a[:]
    b_new = b[:]
    for i in range(len(a_new)):
        if -1 in a_new:
            a_new.remove(-1)
    for i in range(len(b_new)):
        if -1 in b_new:
            b_new.remove(-1)
    l, direct = lcs_len(a_new, b_new)
    lcs = get_lcs(direct, a_new, len(a_new) - 1, len(b_new) - 1)
    return 1-len(lcs) / max(len(a_new),len(b_new))

if __name__ == "__main__":
    a = "abcdabf"
    b = "acdbedbf"
    l, direct = lcs_len(a, b)
    lcs = get_lcs(direct, a, len(a) - 1, len(b) - 1)
    print("the length of lcs is:", l[len(a)][len(b)])
    print("one of the lcs:", "".join(lcs))
    lcs.append(-1)
    print(lcs)