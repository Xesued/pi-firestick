import time

from typing_extensions import Unpack


class Gamepad:
    """docstring for Gamepad"""

    def __init__(self):
        self.mapping = {}
        self.mapping["ABS_HAT0X"] = 0  # up
        self.mapping["ABS_HAT0Y"] = 0  # down
        self.mapping["BTN_A"] = 0
        self.mapping["BTN_B"] = 1
        self.mapping["BTN_X"] = 2
        self.mapping["BTN_Y"] = 3
        # self.mapping["KEY_H"] = 4
        # self.mapping["KEY_U"] = 5
        # self.mapping["KEY_K"] = 6
        # self.mapping["KEY_M"] = 7
        # self.mapping["KEY_Q"] = 8
        # self.mapping["KEY_E"] = 9
        # self.mapping["KEY_R"] = 10
        # self.mapping["KEY_T"] = 11
        # self.mapping["KEY_Y"] = 12
        # self.mapping["KEY_P"] = 13
        # self.mapping["KEY_I"] = 14
        # self.mapping["KEY_O"] = 15
        self.state = [
            0xA1,
            0x03,
            [0, 0, 0, 0],  # , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            0x00,
            0x00,
            0x00,
            0x00,
        ]
        i = 0

    def change_state(self, event):
        evdev_code = ecodes.KEY[event.code]
        if self.mapping.has_key(evdev_code):
            if event.value == 1:
                self.state[2][self.mapping[evdev_code]] = 1
            else:
                self.state[2][self.mapping[evdev_code]] = 0

    def send_key(self, bt):
        if event.type == ecodes.EV_KEY and event.value < 2:
            self.change_state(event)
            print(self.state)
            bt.sendInput(self.state)
