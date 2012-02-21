#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SSDistance import SSDistance 

class WordComparer(object):
    """ generated source for WordComparer

    """

    @classmethod
    def comparescores(self, word1, word2):
        distance = 0
        
        
        if (len(word1)>3) and (len(word2)>3):
            if len(word1) <= len(word2):
                distance = SSDistance.getSimilarity(word1, word2)
            else:
                distance = SSDistance.getSimilarity(word2, word1)

        else:
            if word1 == word2:
                return 1
            else:
                return 0
        
        return distance

