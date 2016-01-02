# PyPiLight
RPC Client / Server for desktop ambient lighting of a Rapsberry Pi connected led strip.

#### Requirements:
###### Client:
* [ZeroRPC](http://www.zerorpc.io) for Python.
* PyQt4 -> sudo apt-get install python-qt4

###### Server:
* [Node.js](http://node-arm.herokuapp.com) on your Raspberry Pi.
* [ZeroRPC ](https://www.npmjs.com/package/zerorpc) for Node.js.
* [rpi-ws2801 ](https://www.npmjs.com/package/rpi-ws2801) for Node.js.

#### Usage:
###### Client:
> Usage: Client.py [Screen #]

###### Server (Raspberry Pi):
> Usage: node Server.js