
from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.components.remote as remote
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.components.remote import (
    PLATFORM_SCHEMA, DOMAIN, ATTR_DEVICE, ATTR_COMMAND, ATTR_ACTIVITY)

REQUIREMENTS = ['broadlink','pycrypto']


SERVICE_LEARN = 'broadlink_learn'
SERVICE_CALL = 'broadlink_call'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.positive_int,
    vol.Required("mac"): cv.string,
})

SERVICE_SCHEMA = vol.Schema({
    vol.Required('commandName'): cv.string,
})

device = None

def setup_platform(hass, config, add_devices, discovery_info=None):

    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    mac  = config.get("mac")
    
    conf_file = hass.config.path('broadlink.conf')
    global device
    device = BroadlinkRemote(host,port,mac,conf_file)

    add_devices([device], True)

    hass.services.register(DOMAIN, SERVICE_LEARN, _learn_service,schema=SERVICE_SCHEMA)
    hass.services.register(DOMAIN, SERVICE_CALL, _call_service,schema=SERVICE_SCHEMA)
    return True

def _apply_service(service, service_func):
    """Internal func for applying a service."""
    command_name = service.data.get('commandName')\
    if(command_name != None and command_name !=""):
        service_func(command_name)


def _learn_service(service):
    _apply_service(service, device.learn)

def _call_service(service):
    _apply_service(service, device.call)


class BroadlinkRemote(Entity):
    def __init__(self, host,port,mac,conf_file):
        import codecs
        import broadlink
        import os.path
        import json

        self._device = broadlink.rm((host, port), mac=bytearray(codecs.decode(mac,'hex')));
        self._device.auth()
        self._ip = host
        self._conf_file = conf_file

        if(os.path.isfile(conf_file)):
            commands_file = open(conf_file, "r")
            self._commands = commands_file.read()
            commands_file.close()
        else:
            self._commands = "{}";
        self._commands = json.loads(self._commands)

    @property
    def name(self):
        return 'broadlink'

    @property
    def state(self):
        return "ok"

    @property
    def ip(self):
        return self._ip

    def learn(self, command_name):
        import codecs
        import time
        import os.path
        import json

        self._device.enter_learning()
        while True:
            time.sleep(1)
            ir_packet = self._device.check_data()
            if (ir_packet != None and codecs.encode(ir_packet,"hex") != "4e6f6e65"):
                break

        self._commands[command_name] = codecs.encode(ir_packet,"hex").decode("utf-8")

        commands_file = open(self._conf_file, "w")
        commands_file.write(json.dumps(self._commands))
        commands_file.close()

    def call(self, command_name):
        import codecs
        
        self._device.send_data(codecs.decode(self._commands[command_name],"hex"))

    def update(self):
        a = 1
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
