# -*- coding: utf-8 -*-
__author__ = 'PCPC'
import re


class RegexUtil:
    def __init__(self, infolist):
        self.reged = []
        for info in infolist:
            self.reged.append(re.compile(info))

    def match_lng_and_lat(self, http_data):
        for rege in self.reged:
            if rege.search(http_data):
                return True

        return False
