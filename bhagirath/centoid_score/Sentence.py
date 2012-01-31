#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Sentence(object):
    """ generated source for Sentence

    """
    number = 0
    text = ''
    tokencount = 0
    tokens = ''
    distance = []
    averagedistance = 0
    averagesimilarity = 0
    isselected = True

    def setDistance(self, distance):
        self.distance = distance

    def setSimilarity(self, similarity):
        self.similarity = similarity

    def setIthDistance(self, i, value):
        self.distance[i] = value

    def setIthSimilarity(self, i, value):
        self.similarity[i] = value

