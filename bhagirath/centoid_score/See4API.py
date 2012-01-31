#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bhagirath.centoid_score.CentroidFinder import CentroidFinder

class See4API(object):
    """ generated source for See4API

    """

    @classmethod
    def main(self, a):
        total_inputs = 5
        inputs = ['' for __idx0 in range(total_inputs)]
        inputs[0] = "meraa bhaarata mahaana"
        inputs[1] = "meraa bhaarata mahaana"
        inputs[2] = "meraa bhaarata"
        inputs[3] = "bhaarata"
        inputs[4] = "meraa bhaarata mahaana"
        centroid = CentroidFinder.getCentroid(inputs)
        print ("centroid", centroid) 
        scores = [int() for __idx0 in range(total_inputs)]
        scores = CentroidFinder.getReputationscores()
        ## for-while
        i = 0
        while i < total_inputs:
            print scores[i]
            i += 1
        isAnotherRunNeeded = CentroidFinder.isIterationNeeded()
        if isAnotherRunNeeded:
            print "No need for another Iteration"
        else:
            print "There is a need for another Iteration"

if __name__ == '__main__':
    import sys
    See4API.main(sys.argv)
