#!/usr/bin/env python

import simplejson as json
import sys
from PyQt4.QtGui import QPixmap, QApplication
from PyQt4 import QtGui
import zerorpc
import time

from Utilities import AutoVivification

class GrabberWidget():

	def __init__(self, xCoord, yCoord, captureWidth, captureHeight, captureDecimation=2):

		""" Class containing a rectangle to define the area of screen capture for a single LED. """

		self.xCoord = xCoord
		self.yCoord = yCoord
		self.captureWidth = captureWidth
		self.captureHeight = captureHeight
		self.captureDecimation = captureDecimation

	def captureRGBValue(self, image, ledPosition):

		""" Averages an RGB value based on the GrabberWidget's rectangle from a given image. """

		totalR = 0
		totalG = 0
		totalB = 0

		pixelCount = 0

		for xIndex in range(self.xCoord, self.captureWidth + self.xCoord, self.captureDecimation):
			for yIndex in range(self.yCoord, self.captureHeight + self.yCoord, self.captureDecimation):

				currentPixel = image.pixel(xIndex, yIndex)

				totalR += QtGui.qRed(currentPixel)
				totalG += QtGui.qGreen(currentPixel)
				totalB += QtGui.qBlue(currentPixel)

				pixelCount += 1

		averageScale = 1.0 / pixelCount

		averageR = totalR * averageScale
		averageG = totalG * averageScale
		averageB = totalB * averageScale

		rgbValue = { 'POS' : ledPosition,
					 'R' : averageR,
					 'G' : averageG,
				     'B' : averageB }

		return rgbValue


class Led():

	def __init__(self, xCoord, yCoord, captureWidth, captureHeight, ledPos):

		""" Class containing all necessary data to for an 'Ambilight LED' """

		self.ledValue = { 'POS' : ledPos,
						  'R' : 0,
						  'G' : 0,
						  'B' : 0 }

		self.positionInStrip = ledPos

		self.captureWidget = GrabberWidget(xCoord, yCoord, captureWidth, captureHeight)

	def updateRGB(self, image):
		self.ledValue = self.captureWidget.captureRGBValue(image, self.ledValue['POS'])

	def getRGB(self):
		return self.ledValue

	def getPosition(self):
		return self.ledValue['POS']

class LedArray():

	def __init__(self, zeroRPCClient, screenWidth, screenHeight, grabberDepth, topLEDCount, bottomLEDCount, leftLEDCount, rightLEDCount, startingSide, rotation=1, captureDecimation=8):
		stripOrder = { 0 : "TOP", 1 : "RIGHT", 2 : "BOTTOM", 3 : "LEFT"}

		self.zeroRPCClient = zeroRPCClient
		self.ledArray = AutoVivification()
		self.app = QApplication(sys.argv)
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight

		leftHeight = screenHeight / leftLEDCount
		rightHeight = screenHeight / rightLEDCount
		topWidth = screenWidth / topLEDCount
		bottomWidth = screenWidth / bottomLEDCount

		ledCount = 0

		for i in range(4):
			currentSide = (startingSide + i) % 4

			if (currentSide == 0):
				for j in range(topLEDCount):
					ledCount += 1
					self.ledArray[stripOrder[currentSide]][j] = Led(j * topWidth, 0, topWidth, grabberDepth, ledCount);

			if (currentSide == 1):
				for j in range(rightLEDCount):
					ledCount += 1
					self.ledArray[stripOrder[currentSide]][j] = Led(screenWidth - grabberDepth, j * rightHeight, grabberDepth, rightHeight, ledCount);

			if (currentSide == 2):
				for j in range(bottomLEDCount):
					ledCount += 1
					print(j * bottomWidth, screenHeight - grabberDepth, bottomWidth, grabberDepth, ledCount)
					self.ledArray[stripOrder[currentSide]][j] = Led((screenWidth - bottomWidth) - (j * bottomWidth), screenHeight - grabberDepth, bottomWidth, grabberDepth, ledCount);

			if (currentSide == 3):
				for j in range(leftLEDCount):
					ledCount += 1
					self.ledArray[stripOrder[currentSide]][j] = Led(0, (screenHeight - leftHeight) - (j * leftHeight), grabberDepth, leftHeight, ledCount);

			if (rotation == -1):
				dict([[k, self.ledArray[stripOrder[currentSide]][len(self.ledArray[stripOrder[currentSide]])-1-k]] for k,v in self.ledArray[stripOrder[currentSide]].iteritems()])

	def updateArray(self, image):

		ledData = AutoVivification()

		for led in self.ledArray["TOP"]:
			self.ledArray["TOP"][led].updateRGB(image)
			ledData[self.ledArray["TOP"][led].getPosition()] = self.ledArray["TOP"][led].getRGB()
			print("Adding Top LEDS.")
		for led in self.ledArray["BOTTOM"]:
			self.ledArray["BOTTOM"][led].updateRGB(image)
			ledData[self.ledArray["BOTTOM"][led].getPosition()] = self.ledArray["BOTTOM"][led].getRGB()
			print("Adding Bottom LEDS.")
		for led in self.ledArray["LEFT"]:
			self.ledArray["LEFT"][led].updateRGB(image)
			ledData[self.ledArray["LEFT"][led].getPosition()] = self.ledArray["LEFT"][led].getRGB()
			print("Adding Left LEDS.")
		for led in self.ledArray["RIGHT"]:
			self.ledArray["RIGHT"][led].updateRGB(image)
			ledData[self.ledArray["RIGHT"][led].getPosition()] = self.ledArray["RIGHT"][led].getRGB()
			print("Adding Right LEDS.")

		self.zeroRPCClient.setLEDS(json.loads(json.dumps(ledData)))


