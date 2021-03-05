import argparse
import json

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
    print(codes)

else:
    print("Lets read in the values")
    # import ir.read
