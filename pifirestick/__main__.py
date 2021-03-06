import argparse
import json

from pifirestick.remote.arcade_stick import ArcadeStick

p = argparse.ArgumentParser()
g = p.add_mutually_exclusive_group(required=True)
g.add_argument("-s", "--start", help="Start up the pi_firestick", action="store_true")
g.add_argument(
    "-r", "--record_ir", help="Start up the pi_firestick", action="store_true"
)

args = p.parse_args()

if args.start:
    print("Time to play")
    try:
        f = open("remote_codes", "r")
    except:
        print("Can't open codes file")
        exit(0)

    codes = json.load(f)
    stick = ArcadeStick.get_arcade() 
    try:
        for key_input in stick.on_input(): 
            print('--- ')
            print(key_input)
            # TODO: Find a method to make this work with edge GPIO detection,
            # or some sort of change detection from the USB.
            # time.sleep(0.1)

    except KeyboardInterrupt:
        sys.exit(0)
else:
    print("Lets read in the values")
    # import ir.read
