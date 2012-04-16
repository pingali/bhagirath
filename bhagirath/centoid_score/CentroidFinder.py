#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Sentence import Sentence
from SentenceTokenizer import SentenceTokenizer
from SentenceMap import SentenceMap
from WordCompararer import WordComparer
from SSDistance import SSDistance
import sys, random

"""
//The inputs are received in the form of two sentences 
//Innocent mistakes - Ordering errors; Suffix errors; tense errors; word missing, added
//Malicious mistakes - To avoid these getting qualified as valid translations 
"""
class CentroidFinder(object):
   
    reputation = []
    normalizedreputation = []
    mapscorematrix=[]
    mapmatrix=[]
    mapweightmatrix=[]
    normalizer = 0
    @classmethod
    def getCentroid(self, a):
        selectedsentnum = 0
        selectedtranslation = ""
        total_num_outputs = len(a)
        sentences = [Sentence() for __idx0 in range(total_num_outputs)]
        self.reputation = [float() for __idx0 in range(total_num_outputs)]
        ## for-while
        i = 0
        while i < total_num_outputs:
            sentences[i] = Sentence()
            self.reputation[i] = 0.0
            i += 1
        ## for-while
        i = 0
        while i < total_num_outputs:
            sentences[i].number = i
            sentences[i].text = a[i]
            sentences[i].tokencount = SentenceTokenizer.tokencount(sentences[i].text)
            sentences[i].tokens = SentenceTokenizer.sentencetokenizer(sentences[i].text)
            sentences[i].setDistance([float() for __idx0 in range(total_num_outputs)])
            sentences[i].setSimilarity([float() for __idx0 in range(total_num_outputs)])
            i += 1
            
        if len(sentences) <= 1:#//if only 1 or 2 candidate translations available
            randomGenerator = random()
            randomchoice = randomGenerator.nextInt(len(sentences))#check
            selectedtranslation = sentences[randomchoice].text
        else:#//if 3 or more candidate translations are available
            total_combinations = (total_num_outputs * (total_num_outputs - 1)) / 2
            #print ("total combo",total_combinations)
            sentencemapcount = 0
            filtercriteria = 0.4
            sentencemaps = [SentenceMap(0,0,0,0,0,0) for __idx0 in range(total_combinations)]
            ## Two for loop to list nC2 combinations
            i = 0
            while i < (len(sentences) - 1):
                ## for-while
                j = i + 1
                while j <= (len(sentences) - 1):
                    sentencemaps[sentencemapcount] = SentenceMap(i, j, sentences[i].tokencount, sentences[j].tokencount, len(sentences[i].text) - sentences[i].tokencount + 1, len(sentences[j].text) - sentences[i].tokencount + 1)
                    a = []
                    for x in range(sentences[i].tokencount):
                        a.append([])
                        for y in range(sentences[j].tokencount):
                            a[x].append(float())
                    self.mapscorematrix = a
                    
                    a = []
                    for x in range(sentences[i].tokencount):
                        a.append([])
                        for y in range(sentences[j].tokencount):
                            a[x].append(float())
                    self.mapmatrix = a
                    
                    a = []
                    for x in range(sentences[i].tokencount):
                        a.append([])
                        for y in range(sentences[j].tokencount):
                            a[x].append(float())
                    self.mapweightmatrix = a
                    ## initializing the matrices 
                    slength1 = 0
                    while slength1 < (sentences[i].tokencount):
                        slength2 = 0
                        while slength2 < (sentences[j].tokencount):
                            self.mapscorematrix[slength1][slength2] = 0
                            self.mapmatrix[slength1][slength2] = 0
                            self.mapweightmatrix[slength1][slength2] = 0
                            slength2 += 1
                        slength1 += 1
                    """
                    print "matrices"
                    print self.mapscorematrix
                    print self.mapmatrix
                    print self.mapweightmatrix
                    """
                    ## set scores for the bipartite graph
                    slength1 = 0
                    while slength1 < sentences[i].tokencount:
                        slength2 = 0
                        while slength2 < sentences[j].tokencount:
                            #print "args"
                            #print (sentences[i].tokens[slength1], sentences[j].tokens[slength2])
                            self.mapscorematrix[slength1][slength2] = WordComparer.comparescores(sentences[i].tokens[slength1], sentences[j].tokens[slength2])
                            #print "self.mapscorematrix[slength1][slength2]" + str(WordComparer.comparescores(sentences[i].tokens[slength1], sentences[j].tokens[slength2]))
                            slength2 += 1
                        slength1 += 1
                    #print ("mapscorematrix",self.mapscorematrix)
                    if sentences[i].tokencount <= sentences[j].tokencount:
                        debaredlist = []
                        ## for-while
                        slength1 = 0
                        while slength1 < sentences[i].tokencount:
                            index2 = -1
                            similarity = filtercriteria
                            ## for-while
                            slength2 = 0
                            while slength2 < sentences[j].tokencount:
                                if ((similarity < self.mapscorematrix[slength1][slength2]) and not (self.iselementpresent(debaredlist, slength2))):
                                    similarity = self.mapscorematrix[slength1][slength2]
                                    index2 = slength2
                                slength2 += 1
                            if (index2 != -1):
                                if len(sentences[i].tokens[slength1]) > len(sentences[j].tokens[index2]):
                                    self.mapweightmatrix[slength1][index2] = len(sentences[j].tokens[index2])
                                else:
                                    self.mapweightmatrix[slength1][index2] = len(sentences[i].tokens[slength1])
                                self.mapmatrix[slength1][index2] = similarity
                                debaredlist.append(index2)
                            slength1 += 1
                    else:
                        debaredlist = []
                        ## for-while
                        slength2 = 0
                        while slength2 < sentences[j].tokencount:
                            index1 = -1
                            similarity = filtercriteria
                            ## for-while
                            slength1 = 0
                            while slength1 < sentences[i].tokencount:
                                if ((similarity < self.mapscorematrix[slength1][slength2]) and not (self.iselementpresent(debaredlist, slength1))):
                                    similarity = self.mapscorematrix[slength1][slength2]
                                    index1 = slength1
                                slength1 += 1
                            if (index1 != -1):
                                if len(sentences[i].tokens[index1]) > len(sentences[j].tokens[slength2]):
                                    self.mapweightmatrix[index1][slength2] = len(sentences[j].tokens[slength2])
                                else:
                                    self.mapweightmatrix[index1][slength2] = len(sentences[i].tokens[index1])
                                self.mapmatrix[index1][slength2] = similarity
                                #print "self.mapmatrix[index1][slength2] : " + str(self.mapmatrix[index1][slength2])correct
                                debaredlist.append(index1)
                            slength2 += 1
                    #print self.mapmatrix
                    sentencemaps[sentencemapcount].setscorematrix(self.mapscorematrix)
                    sentencemaps[sentencemapcount].setmapmatrix(self.mapmatrix)
                    sentencemaps[sentencemapcount].setweightmatrix(self.mapweightmatrix)
                    distance = sentencemaps[sentencemapcount].setsentencesimilarityscore()
                    similarity = sentencemaps[sentencemapcount].sentencesimilarityscore
                    #print (distance,similarity)
                    sentences[i].setIthDistance(j, distance)
                    sentences[j].setIthDistance(i, distance)
                    sentences[i].setIthSimilarity(j, similarity)
                    sentences[j].setIthSimilarity(i, similarity)
                    sentencemapcount += 1
                    j += 1
                i += 1
            ## for-while
            i = 0
            while i < total_num_outputs:
                totaldistance = 0
                totalsimilarity = 0
                ## for-while
                j = 0
                while j < total_num_outputs:
                    totalsimilarity = totalsimilarity + sentences[i].similarity[j]
                    totaldistance = totaldistance + sentences[i].distance[j]
                    #print (totalsimilarity,totaldistance)
                    j += 1
                sentences[i].averagesimilarity = totalsimilarity / (total_num_outputs - 1)
                self.reputation[i] = sentences[i].averagesimilarity
                #print "rep" + str(self.reputation[i])
                sentences[i].averagedistance = totaldistance / (total_num_outputs - 1)
                i += 1
                
            newdistance = 0
            newoptdistance = 1000000000
            ## for-while
            z = 0
            while z < len(sentences):
                ## for-while
                y = 0
                while y < len(sentences):
                    #print sentences[z].distance[y]
                    newdistance = newdistance + sentences[z].distance[y]
                    y += 1
                    
                if newdistance < newoptdistance:
                    selectedsentnum = z
                    selectedtranslation = sentences[z].text
                    newoptdistance = newdistance
                newdistance = 0
                z += 1
        
        self.normalizer = 10*(sentences[selectedsentnum].tokencount)
        #print "normalizer=" + str(self.normalizer)
        return selectedtranslation

    @classmethod
    def iselementpresent(self, al, element):
        ispresent = False
        ## for-while
        i = 0
        while i < len(al):
            if al[i] == element:
                ispresent = True
                return ispresent
            i += 1
        return ispresent

    @classmethod
    def getReputationscores(self):
        maxscore = 0
        self.normalizedreputation = [int() for __idx0 in range(len(self.reputation))]
        ## for-while
        i = 0
        while i < len(self.reputation):
            if maxscore < self.reputation[i]:
                maxscore = self.reputation[i]
            i += 1
        ## for-while
        #print maxscore
        i = 0
        while i < len(self.reputation):
            if maxscore==0 :
                self.normalizedreputation[i] = 0;
            else:
                self.normalizedreputation[i] = int(self.normalizer*(self.reputation[i]/maxscore))
                i += 1
        return self.normalizedreputation

    @classmethod
    def isIterationNeeded(self):
        closeneighbourcount = 0
        normalscore = int(0.9 * self.normalizer)
        i = 0
        while i < len(self.reputation):
            if self.normalizedreputation[i]>=(normalscore):
                closeneighbourcount += 1
            i += 1
        if closeneighbourcount > 2:
            return True
        return False

