# see http://code.activestate.com/recipes/576874-levenshtein-distance/
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)

    matrix = [range(l1 + 1)] * (l2 + 1)
    for zz in range(l2 + 1):
        matrix[zz] = range(zz,zz + l1 + 1)
        for zz in range(0,l2):
            for sz in range(0,l1):
                if s1[sz] == s2[zz]:
                    matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
                else:
                    matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
                    
   
    return matrix[l2][l1]




def fuzzy_substring(needle, haystack):
    """
    Calculates the fuzzy match of needle in haystack,
    using a modified version of the Levenshtein distance
    algorithm.
    The function is modified from the levenshtein function
    in the bktree module by Adam Hupp
    http://ginstrom.com/scribbles/2007/12/01/fuzzy-substring-matching
    -with-levenshtein-distance-in-python/
    """
    m, n = len(needle), len(haystack)

    # base cases
    if m == 1:
        return not needle in haystack
        if not n:
            return m

    row1 = [0] * (n+1)
    for i in range(0,m):
        row2 = [i+1]
        for j in range(0,n):
            cost = ( needle[i] != haystack[j] )

            row2.append( min(row1[j+1]+1, # deletion
                             row2[j]+1, #insertion
                             row1[j]+cost) #substitution
            )
        row1 = row2
        return min(row1)
