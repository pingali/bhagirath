#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SSDistance(object):
   
    theMatchA = ""
    theMatchB = ""

    @classmethod
    def main(self, a):
        sim = SSDistance.getSimilarity("strike", "striking")
        print sim

    @classmethod
    def getSimilarity(self, s1, s2):
        matches = self.getMatch(s1, s2)
        transpositions = self.getTranspositions(s1, s2)
#        print (transpositions,matches)
        similarity = float((2 * matches) - transpositions) / float(len(s1) + len(s2))
        return similarity
        

    @classmethod
    def getMatch(self,s1,s2):
        
        self.theMatchA = ""
        self.theMatchB = ""
        matches = 0
        ## for-while
        i = 0
        while i < len(s1):
            counter = 0
            while i >= 0 and counter <= i:
                if (s1[i] == s2[i - counter]):
                    matches += 1
                    self.theMatchA = self.theMatchA + s1[i]
                    self.theMatchB = self.theMatchB + s2[i]
                counter += 1
            counter = 1
            while i < len(s2) and counter + i < len(s2):
                if (s1[i] == s2[i + counter]):
                    matches += 1
                    self.theMatchA = self.theMatchA + s1[i]
                    self.theMatchB = self.theMatchB + s2[i]
                counter += 1
            i += 1
        #print matches
        return matches

    @classmethod
    def getTranspositions(self, s1, s2):
        transPositions = 0
        #print (self.theMatchA,"test this")
        
        ## for-while
        i = 0
        while i < len(self.theMatchA):
            counter = 0
            while i >= 0 and counter <= i:
                if (self.theMatchA[i] == self.theMatchB[i - counter]) and counter > 0:
                    transPositions += 1
                counter += 1
            counter = 1
            while i < len(self.theMatchB) and counter + i < len(self.theMatchB):
                if (self.theMatchA[i] == self.theMatchB[i + counter]) and counter > 0:
                    transPositions += 1
                counter += 1
            i += 1
        return transPositions

if __name__ == '__main__':
    import sys
    SSDistance.main(sys.argv)
