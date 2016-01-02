var zerorpc = require("zerorpc");
var leds = require('rpi-ws2801');

leds.connect(109);

leds.setColorIndex(2, 1, 0);

process.on( 'SIGINT', function() {
  console.log( "\nGracefully shutting down from SIGINT (Ctrl-C)" );
  // some other closing procedures go here
  leds.clear(); 
  leds.disconnect();
  process.exit( );
})

var server = new zerorpc.Server({
    setLEDS: function(data, reply) {
      for (var led in data){
        leds.setColor(led, [data[led].R, data[led].G, data[led].B]);
      }

      leds.update();

      reply(null, "LEDS Added & Update @ " + Date());
    },
});

server.bind("tcp://0.0.0.0:4242");

console.log("READY");