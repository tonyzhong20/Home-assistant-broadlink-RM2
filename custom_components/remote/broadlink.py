import logging

from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.components.remote as remote
import homeassistant.helpers.config_validation as cv
from homeassistant.components.remote import (DOMAIN)

DATA_BROADLINK = 'broadlink'

DEPENDENCIES = ['broadlink']


SERVICE_CALL = 'broadlink_call'

SERVICE_SCHEMA = vol.Schema({
    vol.Required('commandName'): cv.string,
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
    command_name = service.data.get('commandName')
    if(command_name != None and command_name !=""):
        device.call(command_name)


class BroadlinkRemote(Entity):
    def __init__(self,device):
        self.device = device

    @property
    def name(self):
        return 'broadlink'

    # @property
    # def state(self):
    #     return "ok"

    def call(self, command_name):
        self.device.call(command_name)

    # def update(self):
    #     retur
    #     """Fetch new state data for this light.

    #     This is the only method that should fetch new data for Home Assistant.
    #     """
