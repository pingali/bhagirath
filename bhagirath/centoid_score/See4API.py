#!/usr/bin/env python
# -*- coding: utf-8 -*-
import StringIO
from CentroidFinder import CentroidFinder

class See4API(object):
    """ generated source for See4API

    """

    @classmethod
    def main(self, a):
        total_inputs = 5
        inputs = ['' for __idx0 in range(total_inputs)]
        
        dictionary_filpath = "C:/Students_HCOMP/abc1.txt"
        file1 = open(dictionary_filpath,'r')
        
        strval = ""
        count = 0
        while strval is not None:
            strval = file1.readline()
            if strval=='':
                break
            else:
                inputs[count] = strval.decode("utf-8")
                #print inputs[count]
                count+=1
        file1.close()
        
        centroid = CentroidFinder.getCentroid(inputs)
        print "centroid : " + str(centroid) 
        scores = [int() for __idx0 in range(total_inputs)]
        scores = CentroidFinder.getReputationscores()
      
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
