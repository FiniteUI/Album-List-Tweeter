import os
import json

def __getConfigPath():
    #builds the config file path
    path = os.path.join(os.getcwd(), 'Data')
    if not os.path.isdir(path):
        os.makedirs(path)
    
    path = os.path.join(path, 'config.json')
    return path

def __getConfigJSONDictionary():
    #returns the config json file as a dictionary
    path = __getConfigPath()

    if os.path.exists(path):
        with open(path, 'r+') as f:
            config = json.load(f)
    else:
        config = {}

    return config

def __saveConfigFile(config):
    #updates the config file
    path = __getConfigPath()

    with open(path, 'w') as f:
        json.dump(config, f, indent = 4)

def saveConfigValue(key, value):
    #saves a value to the config file
    config = __getConfigJSONDictionary()

    config[key] = value
    __saveConfigFile(config)

def getConfigValue(key, default=None):
    #returns a value from the config file
    config = __getConfigJSONDictionary()

    if key in config.keys():
        return config[key]
    else:
        return default