import argparse
import json

from ir import IrRemote
from remote.arcade_stick import ArcadeStick

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
    ir_remote = IrRemote(17, codes) 

    try:
        for key_input in stick.read_input(): 
            # Installed joystick sideways
            
            print("key_input: {}".format(key_input))
            if key_input == 'RIGHT':
                ir_remote.send('vol+')

            elif key_input == 'LEFT':
                ir_remote.send('vol-')

            print(key_input)

    except KeyboardInterrupt:
        exit(0)
else:
    print("Lets read in the values")
    # import ir.read
