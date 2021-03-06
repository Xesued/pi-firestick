import evdev

JS_UP = "UP"
JS_DOWN = "DOWN"
JS_LEFT = "LEFT"
JS_RIGHT = "RIGHT"
JS_X_CENTER = "X_CENTER"
JS_Y_CENTER = "Y_CENTER"
BTN_A = "BTN_A"
BTN_B = "BTN_B"
BTN_C = "BTN_C"
BTN_D = "BTN_D"

class ArcadeStick:
  device = None

  @staticmethod
  def get_arcade():
    """
    Gets the remove device
    """
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # TODO: Better method to find the joystick?
    d = next(device for device in devices if device.info.vendor == 121)

    return ArcadeStick(d)
  
  def __init__(self, device):
     self.device = device 

  def read_input(self):
    """
    Calls the function given when there is an input to the arcade stick.  
    
    """
    for event in self.device.read_loop():
      if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_Z:
        continue  # ignore z-axis

      # X axis
      if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_X:
        print(evdev.util.categorize(event))
        if event.value > 200:
          yield JS_RIGHT
        if event.value < 50:
          yield JS_LEFT
        else:
          yield JS_X_CENTER

      # Y axis
      if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_Y:
        print(evdev.util.categorize(event))
        if event.value > 200:
          yield JS_UP
        if event.value < 50:
          yield JS_DOWN
        else:
          yield JS_Y_CENTER

      # Buttons
      if event.type == evdev.ecodes.EV_KEY:
        if event.code == evdev.ecodes.BTN_TRIGGER:
          yield BTN_A
        if event.code == evdev.ecodes.BTN_THUMB:
          yield BTN_B
