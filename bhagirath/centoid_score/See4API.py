#!/usr/bin/env python
# -*- coding: utf-8 -*-
from CentroidFinder import CentroidFinder

class See4API(object):
    """ generated source for See4API

    """

    @classmethod
    def main(self, a):
        total_inputs = 5
        inputs = ['' for __idx0 in range(total_inputs)]
        inputs[0] = "meraa bhaarata mahaana h"
        inputs[1] = ""
        inputs[2] = "meraa bhaarata mahaana "
        inputs[3] = "meraa bhaarata mahaana"
        inputs[4] = "meraa bhaarat hai"
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
