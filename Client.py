#!/usr/bin/env python

import sys
import argparse
import ipaddr
from PyQt4.QtGui import QPixmap, QApplication
from PyQt4 import QtGui
import zerorpc
import time

from Led import LedArray

# Login Information
import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

# Create our PyQt Specific Variables.
qApp = QApplication(sys.argv)
qDesktop = qApp.desktop()

argumentParser = argparse.ArgumentParser()

argumentParser.add_argument('d', help='Screen from which to grab Ambilight data.', type=int)
argumentParser.add_argument('i', help='Raspberry Pi IP hosting our Server.js.')
argumentParser.add_argument('p', help='Raspberry Pi Port hosting our Server.js.', type=int)

arguments = argumentParser.parse_args()

if not (arguments.d in range(qDesktop.numScreens())):
	print('Invalid Display. Available Displays: ')

	for i in range(qDesktop.numScreens()):
		print('Screen # %s %sx%s' % (i, qApp.desktop().screenGeometry(i).width(), qApp.desktop().screenGeometry(i).height()))

	sys.exit('usage: %s [-h] d i p' % sys.argv[0])

try:
	ip = ipaddr.IPAddress(arguments.i)
except ValueError as e:
	print(e)
	sys.exit('usage: %s [-h] d i p' % sys.argv[0])

# Get Screen Geometry for Given Screen.
qScreenRect = qApp.desktop().screenGeometry(arguments.d)

rpcClient = zerorpc.Client("tcp://%s:%s" % (arguments.i, arguments.p))

ledArray = LedArray(rpcClient, qScreenRect.width(), qScreenRect.height(), 64, 34, 34, 21, 21, 3, 1)

while True:

	image = QPixmap.grabWindow(QApplication.desktop().winId(), qScreenRect.x(), qScreenRect.y(), 
								qScreenRect.width(), qScreenRect.height()).toImage()
	
	ledArray.updateArray(image)

	time.sleep(1/20)