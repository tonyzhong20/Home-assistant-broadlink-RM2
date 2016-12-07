# Home-assistant-broadlink-RM2
This is Home-assistant-broadlink-RM2 custom service

broadlink_call
  {"commandName":name}
  
broadlink_learn
  {"commandName":name}



##Config
Put the following config to ~/.homeassistant/configuration.yaml

```
remote:
- platform: broadlink
  host: ''
  port: 80
  mac : ''
```    
Put the code under ~/.homeassistant/custom_components/remote


Work base on https://github.com/mjg59/python-broadlink
