import time
import pigpio

from .common import FREQ, GAP_S


class CommandNotFound(Exception):
    """Base class for exceptions in this module."""

    pass


class IrRemote:
    def __init__(self, gpio_pin, codes):
        self._codes = codes
        self._pin = gpio_pin
        self.pi = pigpio.pi()  # Connect to Pi.

        if not self.pi.connected:
            exit(0)

        self.pi.set_mode(gpio_pin, pigpio.OUTPUT)  # IR TX connected to this GPIO
        self.pi.wave_add_new()

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
                    wf = self._carrier(self._pin, FREQ, ci)
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

    def _carrier(self, gpio, frequency, micros):
        """
        Generate carrier square wave.
        """
        wf = []
        cycle = 1000.0 / frequency
        cycles = int(round(micros / cycle))
        on = int(round(cycle / 2.0))
        sofar = 0
        for c in range(cycles):
            target = int(round((c + 1) * cycle))
            sofar += on
            off = target - sofar
            sofar += off
            wf.append(pigpio.pulse(1 << gpio, 0, on))
            wf.append(pigpio.pulse(0, 1 << gpio, off))
        return wf

    def read(self):
        try:
            f = open(FILE, "r")
            records = json.load(f)
            f.close()
        except:
            records = {}

        pi.set_mode(GPIO, pigpio.INPUT)  # IR RX connected to this GPIO.
        pi.set_glitch_filter(GPIO, GLITCH)  # Ignore glitches.
        cb = pi.callback(GPIO, pigpio.EITHER_EDGE, cbf)

        # Process each id

        print("Recording")
        for arg in args.id:
            print("Press key for '{}'".format(arg))
            code = []
            fetching_code = True
            while fetching_code:
                time.sleep(0.1)
            print("Okay")
            time.sleep(0.5)

            if CONFIRM:
                press_1 = code[:]
                done = False

                tries = 0
                while not done:
                    print("Press key for '{}' to confirm".format(arg))
                    code = []
                    fetching_code = True
                    while fetching_code:
                        time.sleep(0.1)
                    press_2 = code[:]
                    the_same = compare(press_1, press_2)
                    if the_same:
                        done = True
                        records[arg] = press_1[:]
                        print("Okay")
                        time.sleep(0.5)
                    else:
                        tries += 1
                        if tries <= 3:
                            print("No match")
                        else:
                            print("Giving up on key '{}'".format(arg))
                            done = True
                        time.sleep(0.5)
            else:  # No confirm.
                records[arg] = code[:]

        pi.set_glitch_filter(GPIO, 0)  # Cancel glitch filter.
        pi.set_watchdog(GPIO, 0)  # Cancel watchdog.

        tidy(records)

        backup(FILE)

        f = open(FILE, "w")
        f.write(json.dumps(records, sort_keys=True).replace("],", "],\n") + "\n")
        f.close()
