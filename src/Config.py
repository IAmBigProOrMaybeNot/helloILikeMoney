import configparser
import os
# a singleton class that uses configparser to get the config file

CONFIGPATH = r"C:\Users\Luki\PycharmProjects\helloILikeMoney\configB\config.ini"
class Config():
    instance = None
    # PRIVATE CONSTRUCTOR

    @classmethod
    def getConfig(cls, section, key, default):
        print(CONFIGPATH)
        if cls.instance == None:
            cls.instance = configparser.ConfigParser()
            cls.instance.read(CONFIGPATH)
        print(cls.instance)
        return cls.instance[section][key]
