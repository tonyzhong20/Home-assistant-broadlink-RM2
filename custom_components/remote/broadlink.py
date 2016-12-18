from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.components.remote as remote
import homeassistant.helpers.config_validation as cv
from homeassistant.components.remote import (DOMAIN)

DATA_BROADLINK = 'broadlink'

DEPENDENCIES = ['broadlink']


SERVICE_CALL = 'broadlink_call'

SERVICE_SCHEMA = vol.Schema({
    vol.Optional('commandName'): cv.string,
    vol.Required('device'): cv.string,
    vol.Optional('count'): cv.string,
})

device = None

def setup_platform(hass, config, add_devices, discovery_info=None):

    if discovery_info is None:
        return

    broadlink = hass.data[DATA_BROADLINK]
    global device
    device = BroadlinkRemote(broadlink)

    add_devices([device], True)

    hass.services.register(DOMAIN, SERVICE_CALL, _call_service,schema=SERVICE_SCHEMA)
    return True


def _call_service(service):
    _device = service.data.get('device')
    command_name = service.data.get('commandName')
    if(_device != "None" and _device != ""):
        device.call(_device, command_name)


class BroadlinkRemote(Entity):
    def __init__(self,device):
        self.device = device

    @property
    def name(self):
        return 'broadlink'

    def call(self, device, command_name):
        self.device.call(device, command_name)

