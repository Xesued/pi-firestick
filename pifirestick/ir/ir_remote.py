import time
import pigpio
import json

# import os

from .common import (
    FREQ,
    GAP_S,
    POST_MS,
    PRE_US,
    POST_US,
    GLITCH,
    backup,
    tidy,
    carrier,
    cbf,
    compare,
    end_of_code,
)


class CommandNotFound(Exception):
    """Base class for exceptions in this module."""

    pass


class IrRemote:

    pi = pigpio.pi()  # Connect to Pi.
    if not self.pi.connected:
        exit(0)
    pi.set_mode(self._send_pin, pigpio.OUTPUT)  # IR TX connected to this GPIO
    pi.wave_add_new()

    def __init__(self, code_file, send_pin=27, receive_pi=22):
        self._code_file = code_file
        self._codes = self._read_code_file(code_file)
        self._send_pin = send_pin
        self._receive_pin = receive_pi

    @staticmethod
    def _read_code_file(file_name):
        try:
            f = open(file_name, "r")
            return json.load(f)
        except:
            print("Can't open codes file")
            exit(0)

    def send(self, cmd):
        code = self._codes[cmd]
        if not code:
            raise CommandNotFound("Command {} not found.".format(cmd))

        self._wave(code)

    def _wave(self, code):
        # Create wave
        emit_time = time.time()
        marks_wid = {}
        spaces_wid = {}

        wave = [0] * len(code)

        for i in range(0, len(code)):
            ci = code[i]
            if i & 1:  # Space
                if ci not in spaces_wid:
                    self.pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                    spaces_wid[ci] = self.pi.wave_create()
                wave[i] = spaces_wid[ci]
            else:  # Mark
                if ci not in marks_wid:
                    wf = carrier(self._send_pin, FREQ, ci)
                    self.pi.wave_add_generic(wf)
                    marks_wid[ci] = self.pi.wave_create()
                wave[i] = marks_wid[ci]

        delay = emit_time - time.time()

        if delay > 0.0:
            time.sleep(delay)

        self.pi.wave_chain(wave)

        while self.pi.wave_tx_busy():
            time.sleep(0.002)

        emit_time = time.time() + GAP_S

        for i in marks_wid:
            self.pi.wave_delete(marks_wid[i])

        marks_wid = {}

        for i in spaces_wid:
            self.pi.wave_delete(spaces_wid[i])

        spaces_wid = {}

    def read(self, input_names):
        try:
            f = open(FILE, "r")
            records = json.load(f)
            f.close()
        except:
            records = {}

        self.pi.set_mode(
            self._receive_pin, pigpio.INPUT
        )  # IR RX connected to this GPIO.
        self.pi.set_glitch_filter(self._receive_pin, GLITCH)  # Ignore glitches.
        self.pi.callback(self._receive_pin, pigpio.EITHER_EDGE, self.cbf)

        # Process each id

        print("Recording")
        for input_code in input_names:
            print("Press key for '{}'".format(input_code))
            self._incoming_code = []
            fetching_code = True
            while fetching_code:
                time.sleep(0.1)
            print("Okay")
            time.sleep(0.5)

            # if CONFIRM:
            if True:
                press_1 = code[:]
                done = False

                tries = 0
                while not done:
                    print("Press key for '{}' to confirm".format(input_cod))
                    code = []
                    fetching_code = True
                    while fetching_code:
                        time.sleep(0.1)
                    press_2 = code[:]
                    the_same = compare(press_1, press_2)
                    if the_same:
                        done = True
                        records[code] = press_1[:]
                        print("Okay")
                        time.sleep(0.5)
                    else:
                        tries += 1
                        if tries <= 3:
                            print("No match")
                        else:
                            print("Giving up on key '{}'".format(code))
                            done = True
                        time.sleep(0.5)
            # else:  # No confirm.
            #     records[arg] = code[:]

        self.pi.set_glitch_filter(self._receive_pin, 0)  # Cancel glitch filter.
        self.pi.set_watchdog(self._receive_pin, 0)  # Cancel watchdog.

        tidy(records)

        backup(self._code_file)

        f = open(self._code_file, "w")
        f.write(json.dumps(records, sort_keys=True).replace("],", "],\n") + "\n")
        f.close()

    @classmethod
    def cbf(cls, gpio, level, tick):
        # global last_tick, in_code, code, fetching_code
        if level != pigpio.TIMEOUT:
            edge = pigpio.tickDiff(cls.last_tick, tick)
            cls.last_tick = tick

            if cls.fetching_code:

                if (edge > PRE_US) and (not cls.in_code):  # Start of a code.
                    in_code = True
                    cls.pi.set_watchdog(GPIO, POST_MS)  # Start watchdog.

                elif (edge > POST_US) and cls.in_code:  # End of a code.
                    in_code = False
                    cls.pi.set_watchdog(GPIO, 0)  # Cancel watchdog.
                    end_of_code()

                elif in_code:
                    code.append(edge)

        else:
            pi.set_watchdog(GPIO, 0)  # Cancel watchdog.
            if in_code:
                in_code = False
                end_of_code()

    @classmethod
    def end_of_code(cls):
        global code, fetching_code
        if len(cls.input_code) > SHORT:
            normalise(cls.input_code)
            fetching_code = False
        else:
            cls.input_code = []
            print("Short code, probably a repeat, try again")