#-*- coding: utf-8 -*-
'''
Copyright (C) 2012  Diego Torres Milano
Created on May 5, 2012
@author: diego
'''

import sys
import os
import time

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient

def teste():

    vc = ViewClient(*ViewClient.connectToDeviceOrExit())

    for bt in ['One', 'Two', 'Three', 'Four', 'Five']:
        b = vc.findViewWithText(bt)
        if b:
            (x, y) = b.getXY()
            print >>sys.stderr, "clicking b%s @ (%d,%d) ..." % (bt, x, y)
            b.touch()
            b.drag((540.0,528.0), (540.0,1650.2999), 1, 10)
        else:
            print >>sys.stderr, "b%s not found" % bt
        time.sleep(7)

    print >>sys.stderr, "bye"