import argparse
import json
import pigpio

from pifirestick.config import config
from pifirestick.remote.arcade_stick import ArcadeStick
from pifirestick.remote.remote import Remotes, AudioRecieverRemote, TVRemote
from pifirestick.rotary_encoder.rotary import Decoder

p = argparse.ArgumentParser()
g = p.add_mutually_exclusive_group(required=True)
g.add_argument("-s", "--start", help="Start up the pi_firestick", action="store_true")
g.add_argument("-r", "--record", help="Start up the pi_firestick", action="store_true")
p.add_argument("id", nargs="+", type=str, help="IR codes")

args = p.parse_args()


codes_file = "keycodes.json"

if args.start:
    # Setup the Rotary decoder
    pi = pigpio.pi()
    decoder = Decoder(
        pi, 
        int(config['PINS']['DECODER_A']), 
        int(config['PINS']['DECODER_B'])
    )

    # Build the list of remotes we will use
    remote_list = [
        TVRemote(),
        AudioRecieverRemote()
    ]

    remotes = Remotes(decoder, remote_list)

    try:
        remotes.start()

    except KeyboardInterrupt:
        exit(0)

elif args.record:
    from piir.io import receive
    from piir.decode import decode
    from piir.prettify import prettify

    keys = {}

    for keyname in args.id:
        while True:
            data = decode(receive(int(config['PINS']['IR_READ'])))
            if data:
                break
        keys[keyname] = data

    f = open("keycodes.json", "w")
    f.write(json.dumps(prettify(keys), indent=2))
    f.close()