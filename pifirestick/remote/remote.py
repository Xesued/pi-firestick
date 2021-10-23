"""
The remote code.  Maps the different
remotes to the arcade inputs
"""
import asyncio
from pifirestick.remote.arcade_stick import ArcadeStick
from pifirestick.lcd import Lcd


class Remotes:
    current_remote_index = 0
    arcade_stick = None
    selected_remote = None

    def __init__(self, decoder, remotes):
        self.arcade_stick = ArcadeStick.get_arcade()
        self.remotes = remotes
        self.lcd = Lcd()
        self.rotary = decoder
        self.selected_remote = remotes[0]

    def start(self):
        """ Start the remote.  This selects the first remote and 
        sends any arcade stick inputs to that remote.  When the 
        remote changes, show the current remote on the LCD Screen
        """
        print("Staring remote")

        self._listen_to_rotary()

        # This should never return.. never ending generator
        # function.  This will hold the program open
        self._listen_to_arcade_stick()

    def _listen_to_arcade_stick(self):
        for input in self.arcade_stick.read_input():
            print("New input")
            print(input)
            self.selected_remote.on_arcade_input(input)

    def _listen_to_rotary(self):
        self.rotary.set_callback(self.on_rotary_change) 

    def on_rotary_change(self, way):
        self.current_remote_index += way
        selected_remote = self.remotes[self.current_remote_index % len(self.remotes)]

        self.lcd.lcd_clear()
        self.lcd.lcd_display_string(selected_remote.display_name)




class AudioRecieverRemote:
    display_name = "Audio Reciever"
    # TODO
    def on_arcade_input(self, input):
        # TODO
        print('Audio Not implemented')
        print(input)

class TVRemote:
    display_name = "TV"

    def on_arcade_input(self, input):
        # TODO
        print('TV Not implemented')
        print(input)