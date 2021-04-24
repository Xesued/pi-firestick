import argparse
import json

# from pifirestick.bluetooth import *
# from pifirestick.remote.gamepad import Gamepad
from pifirestick.ir import IrRemote

# from pifirestick.remote.arcade_stick import ArcadeStick

p = argparse.ArgumentParser()
g = p.add_mutually_exclusive_group(required=True)
g.add_argument("-s", "--start", help="Start up the pi_firestick", action="store_true")
g.add_argument(
    "-r", "--record_ir", help="Start up the pi_firestick", action="store_true"
)
p.add_argument("id", nargs="+", type=str, help="IR codes")

args = p.parse_args()

ir_remote = IrRemote("remote_codes")

if args.start:
    print("Time to play")

    stick = ArcadeStick.get_arcade()
    bt = Bluetooth("sdp_record.xml", "000508", "Pi\ Gamepad")
    bt.listen()
    gp = Gamepad()

    try:
        for key_input in stick.read_input():
            # TODO: Use a mapping system rather than a swtich.
            # action = get_action(key_input)
            # action.send()

            # Installed joystick sideways
            print("key_input: {}".format(key_input))
            if key_input == "RIGHT":
                ir_remote.send("vol+")

            elif key_input == "LEFT":
                ir_remote.send("vol-")

            elif key_input == "BTN_A":
                ir_remote.send("mute")

            elif key_input == "BTN_B":
                ir_remote.send("pwr")

            print(key_input)

    except KeyboardInterrupt:
        exit(0)
else:
    from piir.io import receive_pi
    from piir.decode import decode
    from piir.prettify import prettify

    keys = args.id
    for keyname in keys:
        while True:
            data = decode(receive(22))
            if data:
                break
        keys[keyname] = data

    f = open("keycodes.json", "w")
    f.write(json.dumps(prettify(keys), indent=2))
    f.close()

    # print("Lets read in the values")
    # ir_remote.read(args.id)
