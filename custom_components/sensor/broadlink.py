
from homeassistant.helpers.entity import Entity
from homeassistant.const import TEMP_FAHRENHEIT

DATA_BROADLINK = 'broadlink'

DEPENDENCIES = ['broadlink']

def setup_platform(hass, config, add_devices, discovery_info=None):
    if discovery_info is None:
        return

    broadlink = hass.data[DATA_BROADLINK]

    device = BroadlinkSensor(broadlink)

    add_devices([device], True)

    return True

class BroadlinkSensor(Entity):
    
    def __init__(self, device):
        """Initialize the sensor."""
        self.device = device

        # device specific
        self._name = "Broadlink"
        self._state = None
        self._unit = None

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        return TEMP_FAHRENHEIT

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        state = self.device.check_temperature()
        if(state):
            self._state = state