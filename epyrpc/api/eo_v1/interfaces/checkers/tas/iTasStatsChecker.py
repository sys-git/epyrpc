'''
Created on 16 Jul 2012

@author: francis
'''

from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTasStatsChecker(iApi):
    def TestStatsChange(self, i_stats_result):
        raise NotImplementedException("iTasStatsChecker.TestStatsChange")
