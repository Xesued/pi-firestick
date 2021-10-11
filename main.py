import argparse
import json
import time
import pigpio
import asyncio

# from pifirestick.bluetooth import *
# from pifirestick.remote.gamepad import Gamepad
from pifirestick.remote.arcade_stick import ArcadeStick
from pifirestick.remote.remote import Remotes, AudioRecieverRemote, TVRemote
from pifirestick.rotary_encoder.rotary import Decoder
from pifirestick.lcd import Lcd

p = argparse.ArgumentParser()
g = p.add_mutually_exclusive_group(required=True)
g.add_argument("-s", "--start", help="Start up the pi_firestick", action="store_true")
g.add_argument("-r", "--record", help="Start up the pi_firestick", action="store_true")
g.add_argument("-b", "--bluetooth", help="Setup bluetooth", action="store_true")

p.add_argument("id", nargs="+", type=str, help="IR codes")

args = p.parse_args()

codes_file = "keycodes.json"

if args.start:
    import piir
    from pifirestick.lcd import Lcd

    # Setup the Rotary decoder
    pi = pigpio.pi()
    decoder = Decoder(pi, 17, 18)


    # Build the list of remotes we will use
    remote_list = [
        TVRemote(),
        AudioRecieverRemote()
    ]
    remotes = Remotes(decoder, remote_list)

    
    # remote = piir.Remote(codes_file, 27)

    async def start():
        await remotes.start()

    try:
        asyncio.run(start())
        # remotes.start()
            # lcd.lcd_display_string("Sending command:", 1)
            # lcd.lcd_display_string("Mute...", 2)
            # remote.send("mute")
            # time.sleep(1)

            # lcd.lcd_clear()
            # time.sleep(2)

    except KeyboardInterrupt:
        exit(0)

elif args.record:
    from piir.io import receive
    from piir.decode import decode
    from piir.prettify import prettify

    keys = {}

    for keyname in args.id:
        while True:
            data = decode(receive(22))
            if data:
                break
        keys[keyname] = data

    f = open("keycodes.json", "w")
    f.write(json.dumps(prettify(keys), indent=2))
    f.close()

else:
    from pifirestick.bluetooth import lookUpNearbyBluetoothDevices, receiveMessages

    # receiveMessages()
    devices = lookUpNearbyBluetoothDevices()
    print(devices)