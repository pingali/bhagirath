#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SentenceTokenizer(object):
    """ generated source for SentenceTokenizer

    """

    @classmethod
    def tokencount(self, sentence):
        count = 0
        token = sentence.split(" ")
      # print len(token)
        return len(token)

    @classmethod
    def sentencetokenizer(self, sentence):
        sentence = sentence.rstrip('\n')
        token = sentence.split(" ")
        return token

