#!/usr/bin/env python
"""
Given the content distribution file and request trace, calculate
the hit rate and footprint reduction.

Usage: app.py request_trace cache_trace chunk_trace

Liang Wang @ Dept. of Computer Science, University of Helsinki, Finland
2013.02.21
"""

import os
import sys
import networkx as nx

from numpy import *


def construct_topology():
    edgelist = [(0,1), (1,2), (1,3), (2,4), (2,5), (3,6), (3,7),\
                    (4,8), (4,9), (5,10), (5,11), (6,12), (6,13), (7,14), (7,15)]
    G = nx.Graph(edgelist)
    return G

def load_request(ifn):
    # print "load request trace ..."
    request = []
    for line in open(ifn, 'r').readlines():
        f, c = line.split()
        request.append([int(f), int(c)])
    return array(request)

def load_cache(ifn):
    # print "load cache trace ..."
    lines = open(ifn, 'r').readlines()
    files, chunks, routers = get_model_parameter(lines)
    cache = zeros((files+1, chunks+1, routers+1, routers+1))
    for line in lines:
        x, y, u, v, c = line.strip().split()
        cache[int(x), int(y), int(u), int(v)] = c
    return cache

def load_chunk(ifn):
    # print "load chunk info ..."
    lines = open(ifn, 'r').readlines()
    files, chunks = (0, 0)
    for line in lines:
        x, y, s, t = line.strip().split()
        files = max(files, int(x))
        chunks = max(chunks, int(y))
    chunk = zeros((files + 1, chunks + 1))
    for line in lines:
        x, y, s, t = line.split()
        chunk[int(x)][int(y)] = float(s)
    return chunk

def get_model_parameter(lines):
    files, chunks, routers = (0, 0, 0)
    for line in lines:
        x, y, z, _, _ = line.strip().split()
        files = max(files, int(x))
        chunks = max(chunks, int(y))
        routers = max(routers, int(z))
    return files, chunks, routers

def calculate_performance(G, node, request, cache, chunk, index):
    N, P, M, _ = cache.shape
    integral = True if P == 1 else False
    # print "calculating performance ... [%s caching]" % ( "integral" if integral else "partial" )
    HR = 0.0
    byteHR = 0.0
    totalByte = 0.0
    FP = 0.0
    totalFP = 0.0
    FPR = 0.0

    dDE = calculate_document_download_effort(G, node, cache, index)
    #print node, "---->", HR, byteHR, FPR, dDE
    return HR, byteHR, FPR, dDE

def calculate_document_download_effort(G, node, cache, index):
    dEffort = 0.0
    N, P, M, _ = cache.shape
    N = 1
    for i in range(index, index+1):
        tde = 0.0
        for j in range(P):
            tpath = nx.diameter(G) + 1
            for x in where(cache[i,j,node]==1)[0]:
                y = len(nx.shortest_path(G, node, x))
                if tpath > y:
                    tpath = y
            tde += tpath
        dEffort += tde
    dEffort /= N * P * (nx.diameter(G) + 1)
    return dEffort

def calculate_average_performance(G, request, cache, chunk, index):
    nodes = range(8, 16)
    HR, byteHR, FPR, dDE = 0.0, 0.0, 0.0, 0.0
    for n in nodes:
        tHR, tbyteHR, tFPR, tdDE = calculate_performance(G, n, request, cache, chunk, index)
        HR += tHR
        byteHR += tbyteHR
        FPR += tFPR
        dDE += tdDE
    HR /= len(nodes)
    byteHR /= len(nodes)
    FPR /= len(nodes)
    dDE /= len(nodes)
    return HR, byteHR, FPR, dDE

def test_fn(G, request, cache, chunk):
    for i in range(0, 100, 10):
        HR, byteHR, FPR, dDE = calculate_average_performance(G, request, cache, chunk, i)
        print i, dDE
    pass

# Main function

if __name__ == "__main__":
    G = construct_topology()
    request = load_request(sys.argv[1])
    cache = load_cache(sys.argv[2])
    chunk = load_chunk(sys.argv[3])
    test_fn(G, request, cache, chunk)

    sys.exit(0)