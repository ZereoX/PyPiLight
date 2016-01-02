#!/usr/bin/env python

import sys
import argparse
from PyQt4.QtGui import QPixmap, QApplication
from PyQt4 import QtGui
import zerorpc
import time

from Utilities import AutoVivification
from Led import LedArray

# Login Information
import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

# Create our PyQt Specific Variables.
qApp = QApplication(sys.argv)
qDesktop = qApp.desktop()

# Check Sys Arguments.
if (len(sys.argv)) < 2:
    sys.exit('Usage: %s [Screen #]' % sys.argv[0])

if int(sys.argv[1]) in range(qApp.desktop().numScreens()):
	print("Valid")
else:
	for i in range(qApp.desktop().numScreens()):
		print('Screen # %s %sx%s' % (i, qApp.desktop().screenGeometry(i).width(), qApp.desktop().screenGeometry(i).height()))
	sys.exit('Usage: %s [Screen #]' % sys.argv[0])

# Get Screen Geometry for Given Screen.
qScreenRect = qApp.desktop().screenGeometry(int(sys.argv[1]))

# LED Setup Information.
LEDCount = {'LEFT' : 21, 'TOP' : 34, 'RIGHT' : 21, 'BOTTOM' : 34, 'TOTAL' : 110}

c = zerorpc.Client("tcp://192.168.0.105:4242")

ledArray = LedArray(c, qScreenRect.width(), qScreenRect.height(), 64, 34, 34, 21, 21, 3, 1)

while True:

	image = QPixmap.grabWindow(QApplication.desktop().winId(), qScreenRect.x(), qScreenRect.y(), 
								qScreenRect.width(), qScreenRect.height()).toImage()
	
	ledArray.updateArray(image)

	time.sleep(1/20)