
if isDevelop:
  import mock_gpio as GPIO

else:
  import RPio.GPIO
