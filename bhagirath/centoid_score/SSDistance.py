#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SSDistance(object):
    """ generated source for SSDistance

    """
    matchmatrix = []

    @classmethod
    def main(self, a):
        sim = SSDistance.self.getSimilarity("meraa", "bharat")
        print sim

    @classmethod
    def getSimilarity(self, s1, s2):
        self.formMatchMatrix(s1, s2)
        matches = self.getMatches(s1, s2)
        transpositions = self.getTranspositions(s1, s2)
        similarity = float((2 * matches) - transpositions) / float(len(s1) + len(s2))
        return similarity

    @classmethod
    def formMatchMatrix(self, s1, s2):
        a = []
        for x in range(len(s1)):
            a.append([])
            for y in range(len(s2)):
                a[x].append(int())
        self.matchmatrix = a
     
        i = 0
        while i < len(s1):
            j = 0
            while j < len(s2):
                if s1[i] == s2[j]:
                    self.matchmatrix[i][j] = 1
                j += 1
            i += 1

    @classmethod
    def getMatches(self, s1, s2):
        matches = 0
        i = 0
        while i < len(s1):
            point = 0
            j = 0
            while j < len(s2):
                point = point + self.matchmatrix[i][j]
                j += 1
            if point >= 1:
                matches += 1
            i += 1
        return matches

    @classmethod
    def getTranspositions(self, s1, s2):
        transPositions = 0
        forwardMatches = 0
        oldi = -1
        oldj = -1
        i = 0
        while i < len(s1):
            j = 0
            while j < len(s2):
                if (s1[i] == s2[j]):
                    if i > oldi and j > oldj:
                        forwardMatches += 1
                        oldi = i
                        oldj = j
                j += 1
            i += 1
        transPositions = self.getMatches(s1, s2) - forwardMatches
        return transPositions

if __name__ == '__main__':
    import sys
    SSDistance.main(sys.argv)