#!/usr/bin/env python

'''
TODO: add docs
'''
from fireworks.core.firetask import FireTaskBase
from fireworks.utilities.fw_serializers import FWSerializable
from fireworks.core.firework import FireWork
import os

__author__ = 'Anubhav Jain'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Anubhav Jain'
__email__ = 'ajain@lbl.gov'
__date__ = 'Feb 17, 2013'


class AdderTask(FireTaskBase, FWSerializable):
    
    _fw_name = "Addition Task"
    
    def run_task(self, fw):
        input_array = fw.fw_spec['sum']
        m_sum = sum(input_array)

        with open('sum_outputs.txt', 'w') as f:
            f.write("The sum of {} is: {}".format(input_array, m_sum))
        
        return {"sum": m_sum}

if __name__ == '__main__':
    fw = FireWork(AdderTask({}), {"sum": [1, 2]})
    fw.to_file("fw_adder.yaml")