#!/usr/bin/env python
import pigpio

# from RPi import GPIO
# from time import sleep

# CLK = 17
# DT = 18

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# counter = 0
# clkLastState = GPIO.input(CLK)

# try:
#     while True:
#         clkState = GPIO.input(CLK)
#         dtState = GPIO.input(DT) 
#         if clkState != clkLastState:
#             if dtState != clkState:
#                 counter += 1
#             else:
#                 counter -= 1

#             print counter

#         clkLastState = clkState
#         sleep(0.01)

# finally:
#     GPIO.cleanup()



class Decoder:
   callback = None

   """Class to decode mechanical rotary encoder pulses."""

   def __init__(self, pi, gpioA, gpioB):

      """
      Instantiate the class with the pi and gpios connected to
      rotary encoder contacts A and B.  The common contact
      should be connected to ground.  The callback is
      called when the rotary encoder is turned.  It takes
      one parameter which is +1 for clockwise and -1 for
      counterclockwise.

      EXAMPLE

      import time
      import pigpio

      import rotary_encoder

      pos = 0

      def callback(way):

         global pos

         pos += way

         print("pos={}".format(pos))

      pi = pigpio.pi()

      decoder = rotary_encoder.decoder(pi, 7, 8, callback)

      time.sleep(300)

      decoder.cancel()

      pi.stop()

      """

      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

   def set_callback(self, callback):
      self.callback = callback

   def _pulse(self, gpio, level, tick):
      if self.callback == None:
         return

      """
      Decode the rotary encoder pulse.

                   +---------+         +---------+      0
                   |         |         |         |
         A         |         |         |         |
                   |         |         |         |
         +---------+         +---------+         +----- 1

             +---------+         +---------+            0
             |         |         |         |
         B   |         |         |         |
             |         |         |         |
         ----+         +---------+         +---------+  1
      """

      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               self.callback(1)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(-1)

   def cancel(self):

      """
      Cancel the rotary encoder decoder.
      """

      self.cbA.cancel()
      self.cbB.cancel()

if __name__ == "__main__":

   import time
   import pigpio

#    import rotary_encoder

   pos = 0

   def callback(way):

      global pos

      pos += way

      print("pos={}".format(pos))

   pi = pigpio.pi()

   decoder = Decoder(pi, 17, 18)
   decoder.set_callback(callback)

   time.sleep(300)

   decoder.cancel()

   pi.stop()


