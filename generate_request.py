#!/usr/bin/env python
"""
Generate request sequence

2013.01.18
"""

import os
import sys

from numpy import *

# Model constants

SEED = 555  # Random seed for the simulation
N = 1000     # Number of files
P = 10     # Number of chunks in a file
R = 100000  # Number of requests

def request_weibull():
    reqFile = []
    reqChunk = []
    shiftF = 10
    shiftC = 1
    while(True):
        x = random.weibull(0.513) * 40
        if x > shiftF and x < N+shiftF:
            reqFile.append(x-shiftF)
        if len(reqFile) >= R:
            break
    while(True):
        x = random.weibull(0.8) * 40
        if x > shiftC and x < P+shiftC:
            reqChunk.append(x-shiftC)
        if len(reqChunk) >= R:
            break
    return array(reqFile), array(reqChunk)

def output_request(reqFile, reqChunk):
    norma, normb = 1.0, 1.0
    for i in range(R):
        print (int) (reqFile[i] * norma), (int) (reqChunk[i] * normb)
    pass


# Main function

if __name__ == "__main__":
    random.seed(SEED)
    rf, rc = request_weibull()
    output_request(rf, rc)

    sys.exit(0)
