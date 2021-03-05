def read_ir():
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


print("read thist")
print(__name__)