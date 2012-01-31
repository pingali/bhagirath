#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SentenceMap(object):
    """ generated source for SentenceMap

    """
    sentencemapscorematirx = []
    sentencemap = []
    sentenceweightmap = []
    sentenceNumber1 = 0
    sentenceNumber2 = 0
    tokencount1 = 0
    tokencount2 = 0
    charcount1 = 0
    charcount2 = 0
    sentencesimilarityscore = float()
    distance = float()

    def __init__(self, sentenceNum1, sentenceNum2, tcount1, tcount2,ccount1,ccount2):
        self.sentenceNumber1 = sentenceNum1
        self.sentenceNumber2 = sentenceNum2
        self.tokencount1 = tcount1
        self.tokencount2 = tcount2
        self.charcount1 = ccount1
        self.charcount2 = ccount2
       
    def setscorematrix(self, sentencemapscorematrix1):
        a = []
        for i in range(self.tokencount1):
            a.append([])
            for j in range(self.tokencount2):
                a[i].append(float())
        sentencemapscorematrix = a
        self.sentencemapscorematrix = sentencemapscorematrix1

    def setmapmatrix(self, sentencemap1):
        a = []
        for i in range(self.tokencount1):
            a.append([])
            for j in range(self.tokencount2):
                a[i].append(bool())
        sentencemap = a
        #insert logic for matrix corrector to remove ambiguity. Here we assume each row has only on true value. 
        self.sentencemap = sentencemap1
        
    def setweightmatrix(self, sentenceweightmap1):
        a = []
        for i in range(self.tokencount1):
            a.append([])
            for j in range(self.tokencount2):
                a[i].append(bool())
        sentenceweightmap = a
        #insert logic for matrix corrector to remove ambiguity. Here we assume each row has only on true value. 
        self.sentenceweightmap = sentenceweightmap1

    def setsentencesimilarityscore(self):
        matches = self.getmatches()
        transpositions = self.gettranspositions()
        if (matches == 0):#toavoid divide by zero error - early return
            self.sentencesimilarityscore = 0
            self.distance = 2000
            return self.distance
        self.sentencesimilarityscore = ((2 * matches) - transpositions) / float(self.charcount1 + self.charcount2) 
        self.distance = 1 / self.sentencesimilarityscore
       # print "distance is:" + str(self.distance)
        return self.distance

    def getmatches(self):
        matches = 0
        ## for-while
        i = 0
        while i < self.tokencount1:
            ## for-while
            j = 0
            while j < self.tokencount2:
                if self.sentencemap[i][j] > 0:
                    matches = matches + self.sentencemap[i][j] * self.sentenceweightmap[i][j]
                j += 1
            i += 1
        return matches

    def gettranspositions(self):
        transpositions = 0
        oldi = -1
        oldj = -1
        ## for-while
        i = 0
        while i < self.tokencount1:
            ## for-while
            j = 0
            while j < self.tokencount2:
                 if self.sentencemap[i][j] > 0:
                    if i > oldi or j > oldj:
                        if ((i > oldi and j < oldj) or( i < oldi and j > oldj)):
                            transpositions = transpositions + self.sentencemap[i][j] * self.sentenceweightmap[i][j]
                        oldi = i
                        oldj = j
                 j += 1
            i += 1
        return transpositions

