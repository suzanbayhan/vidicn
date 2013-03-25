#!/usr/bin/env python
# 
# This script implements the CachedBit caching strategy.
#
# Liang Wang @ Dept. Computer Science, University of Helsinki, Finland
# 2011.05.31 created
#

import os
import sys
import time
import binascii
from ctypes import *
from router.common import *
from messageheader import *
import random

class vidicn_heuristic_0(object):
    def __init__(self, router, cachesize):
        self.router = router  # Cache's corresponding router
        self.cache = None
        self.logfh = None
        pass

    def ihandler(self, hdr, router):
        hdr.hop += 1
        fil = hdr.fil
        chk = hdr.chk
        cid = (fil, chk)
        siz = hdr.siz
        src = hdr.src
        dst = hdr.dst

        if hdr.type == MessageType.REQUEST:
            if self.cache.is_hit(cid):
                logme3(self.logfh, hdr.seq, src, dst, "REQ", 1, fil, chk)
                hdr.type = MessageType.RESPONSE
                hdr.swap_src_dst()
                hdr.hit = 1
                chunk = self.cache.get_chunk(cid, random.random())
                hdr.siz = chunk['size']

            else:
                logme3(self.logfh, hdr.seq, src, dst, "REQ", 0, fil, chk)
                pass

        elif hdr.type == MessageType.RESPONSE:
            logme3(self.logfh, hdr.seq, src, dst, "RSP", 0, fil, chk)
            evict = self.cache.add_chunk(cid, random.random(), siz)
            #if evict[0]:
            #    logme2(self.logfh, hdr.seq, src, dst, "DEL", 0, evict[0])
            logme3(self.logfh, hdr.seq, src, dst, "ADD", 0, fil, chk)
        if self.router.vrid==1:
            print "*"*30, self.cache.cache.shape, self.cache.usedc

        return False


if __name__ == "__main__":
    print sys.argv[0]
    sys.exit(0)
