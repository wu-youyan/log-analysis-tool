# -*- coding:utf-8 -*-
import configparser


class ConfigOper:
    """get config from the ini file"""
    def __init__(self, config_file):
        self.config = configparser.RawConfigParser()
        self.config.read(config_file,'utf-8')
        self.configFile = config_file
    def set(self, section, option,value):
    	res = self.config.set(section, option, value)
    	return res
    def get(self, section, value):
    	res = self.config.get(section, value)
    	return res
    def addSection(self, section):
    	res = self.config.add_section(section)
    	return res
    def deleteSection(self, section):
    	res = self.config.delete_section(section)
    	return res
    def hasSection(self, section):
    	res = self.config.has_section(section)
    	return res 
    def sections(self):
    	res = self.config.sections()
    def options(self,section):
    	res = self.config.options(section)
    	return res 
    def hasOption(self, section, option):
    	res = self.config.has_option(section, option)
    	return res
    def save(self):
    	self.config.write(open(self.configFile, "w"))
