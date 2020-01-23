from pi_mqtt_gpio.modules import GenericGPIO, PinDirection, PinPullup

ALLOWED_BOARDS = [
    'zero', 'r1', 'zeroplus', 'zeroplus2h5', 'zeroplus2h3',
    'pcpcplus', 'one', 'lite', 'plus2e', 'pc2', 'prime'
]
REQUIREMENTS = ("OrangePi.GPIO",)
CONFIG_SCHEMA = {
    "board": {
        "type": "string",
        "required": True,
        "empty": False,
        "allowed": ALLOWED_BOARDS + list(map(str.upper, ALLOWED_BOARDS))
    }
}

DIRECTIONS = None
PULLUPS = None


class GPIO(GenericGPIO):
    """
    Implementation of GPIO class for Orange Pi native GPIO.
    """

    def __init__(self, config):
        global DIRECTIONS, PULLUPS
        import OPi.GPIO as gpio

        self.io = gpio
        DIRECTIONS = {PinDirection.INPUT: gpio.IN, PinDirection.OUTPUT: gpio.OUT}

        PULLUPS = {
            PinPullup.OFF: gpio.PUD_OFF,
            PinPullup.UP: gpio.PUD_UP,
            PinPullup.DOWN: gpio.PUD_DOWN,
        }

        board = config["board"].upper()
        if not hasattr(gpio, board):
            raise AssertionError("%s board not found" % board)
        gpio.setboard(getattr(gpio, board))
        gpio.setmode(gpio.BCM)

    def setup_pin(self, pin, direction, pullup, pin_config):
        direction = DIRECTIONS[direction]

        if pullup is None:
            pullup = PULLUPS[PinPullup.OFF]
        else:
            pullup = PULLUPS[pullup]

        initial = {None: -1, "low": 0, "high": 1}[pin_config.get("initial")]
        self.io.setup(pin, direction, pull_up_down=pullup, initial=initial)

    def set_pin(self, pin, value):
        self.io.output(pin, value)

    def get_pin(self, pin):
        return self.io.input(pin)

    def cleanup(self):
        self.io.cleanup()
