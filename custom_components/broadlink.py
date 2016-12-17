import voluptuous as vol
import logging
from homeassistant.const import CONF_HOST, CONF_PORT
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery

REQUIREMENTS = ['broadlink','pycrypto']

DOMAIN = 'broadlink'
CONFIG_SCHEMA =  vol.Schema({
    DOMAIN: vol.Schema({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.positive_int,
    vol.Required("mac"): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

DATA_BROADLINK = 'broadlink'

SERVICE_LEARN = 'broadlink_learn'
SERVICE_SCHEMA = vol.Schema({
    vol.Required('commandName'): cv.string,
})

_LOGGER = logging.getLogger(__name__)

SWITCH_PREFIX = 'switch'

def setup(hass, config):
    conf = config[DOMAIN]
    host = conf.get(CONF_HOST)
    port = conf.get(CONF_PORT)
    mac  = conf.get("mac")
    
    conf_file = hass.config.path('broadlink.conf')

    hass.data[DATA_BROADLINK]  = BroadlinkRM2(host,port,mac,conf_file)

    _LOGGER.debug("proceeding with discovery")
    discovery.load_platform(hass, 'remote', DOMAIN, {}, config)
    discovery.load_platform(hass, 'sensor', DOMAIN, {}, config)
    discovery.load_platform(hass, 'switch', DOMAIN, {}, config)

    hass.services.register(DOMAIN, SERVICE_LEARN, _learn_service,schema=SERVICE_SCHEMA)

    _LOGGER.debug("setup done")

    return True

def _learn_service(service):
    command_name = service.data.get('commandName')
    if(command_name != None and command_name !=""):
        hass.data[DATA_BROADLINK].learn(command_name)


class BroadlinkRM2(object):
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

    def check_temperature(self):
        if(self._device):
            return round(self._device.check_temperature()* 1.8 + 32, 2)

    def get_switch_devices(self):
        devices = []
        for device in self._commands:
            if(device.find(SWITCH_PREFIX)==0):
                device = device.split("_")
                device.remove(SWITCH_PREFIX)
                device = " ".join(device)
                devices.extend([device])
        return devices

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

    def call(self, command_name,isSwitch=False):
        import codecs
        if(isSwitch):
            command_name = '{}_{}'.format(SWITCH_PREFIX,command_name)
        self._device.send_data(codecs.decode(self._commands[command_name],"hex"))
