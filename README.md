# Home-assistant-broadlink-RM2
This is Home-assistant-broadlink-RM2 custom service
broadlink_call
  {"commandName":name}
broadlink_learn
  {"commandName":name}

Work base on https://github.com/mjg59/python-broadlink

#Config
Put the following config to ~/.homeassistant/configuration.yaml

remote:
  - platform: broadlink
    host: '192.168.1.126'
    port: 80
    mac : '59f9ee0d43b4'
    
Put the code under ~/.homeassistant/custom_components/remote
