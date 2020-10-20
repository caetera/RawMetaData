# -*- coding: utf-8 -*-
from collections import namedtuple

Method = namedtuple("Method", ["Name", "Text"])

def methods_from_raw(rawFile):
    """
    Extract text representation of all methods from raw file
    """
    nmeth = rawFile.InstrumentMethodsCount
    method_names = rawFile.GetAllInstrumentFriendlyNamesFromInstrumentMethod()
    
    methods = []
    
    for n in range(nmeth):
        methods.append(Method(Name=method_names[n], Text=rawFile.GetInstrumentMethod(n)))
        
    return methods