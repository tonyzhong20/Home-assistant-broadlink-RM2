
from homeassistant.components.switch import SwitchDevice

DATA_BROADLINK = 'broadlink'

DEPENDENCIES = ['broadlink']

def setup_platform(hass, config, add_devices, discovery_info=None):

    if discovery_info is None:
        return

    broadlink = hass.data[DATA_BROADLINK]
    devices = []
    for device in broadlink.get_switch_devices():
        devices.extend([BroadlinkSwitch(broadlink,device,False)])

    add_devices(devices, True)

    return True


class BroadlinkSwitch(SwitchDevice):
    def __init__(self,device, name, state):
        self.device = device
        self._name = name
        self._state = state

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def assumed_state(self):
        """Return if the state is based on assumptions."""
        return self._state

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self.call()
        self._state = False

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self.call()
        self._state = True

    def call(self):
        self.device.call(self._name)
