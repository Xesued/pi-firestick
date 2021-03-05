from .common import FILE


def play():
    try:
        f = open(FILE, "r")
    except:
        print("Can't open: {}".format(FILE))
        exit(0)

    records = json.load(f)

    f.close()

    pi.set_mode(GPIO, pigpio.OUTPUT)  # IR TX connected to this GPIO.

    pi.wave_add_new()

    emit_time = time.time()

    if VERBOSE:
        print("Playing")

    for arg in args.id:
        if arg in records:

            code = records[arg]

            # Create wave

            marks_wid = {}
            spaces_wid = {}

            wave = [0] * len(code)

            for i in range(0, len(code)):
                ci = code[i]
                if i & 1:  # Space
                    if ci not in spaces_wid:
                        pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                        spaces_wid[ci] = pi.wave_create()
                    wave[i] = spaces_wid[ci]
                else:  # Mark
                    if ci not in marks_wid:
                        wf = carrier(GPIO, FREQ, ci)
                        pi.wave_add_generic(wf)
                        marks_wid[ci] = pi.wave_create()
                    wave[i] = marks_wid[ci]

            delay = emit_time - time.time()

            if delay > 0.0:
                time.sleep(delay)

            pi.wave_chain(wave)

            if VERBOSE:
                print("key " + arg)

            while pi.wave_tx_busy():
                time.sleep(0.002)

            emit_time = time.time() + GAP_S

            for i in marks_wid:
                pi.wave_delete(marks_wid[i])

            marks_wid = {}

            for i in spaces_wid:
                pi.wave_delete(spaces_wid[i])

            spaces_wid = {}
        else:
            print("Id {} not found".format(arg))