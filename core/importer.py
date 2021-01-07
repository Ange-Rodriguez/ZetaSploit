#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sys
import time
import json
import threading
import os
import string

from core.db import db
from core.badges import badges
from core.storage import storage
from core.helper import helper
from core.config import config
from core.modules import modules
from core.exceptions import exceptions

class importer:
    def __init__(self):
        self.db = db()
        self.badges = badges()
        self.storage = storage()
        self.helper = helper()
        self.config = config()
        self.modules = modules()
        self.exceptions = exceptions()

    def get_module(self, mu, name, folderpath):
        folderpath_list = folderpath.split(".")
        for i in dir(mu):
            if i == name:
                pass
                return getattr(mu, name)
            else:
                if i in folderpath_list:
                    i = getattr(mu, i)
                    return self.get_module(i, name, folderpath)

    def import_check(self, module_name):
        try:
            __import__(module_name)
        except ModuleNotFoundError:
            return False
        except:
            return True
        return True
        
    def import_command(self, command_path):
        try:
            command_directory = command_path
            command_file = os.path.split(command_directory)[1]
            command_directory = command_directory.replace('/', '.')
            command_object = __import__(command_directory)
            command_object = self.get_module(command_object, command_file, command_directory)
            command_object = command_object.ZetaSploitCommand()
        except:
            raise self.exceptions.GlobalException
        return command_object
        
    def import_module(self, module_path):
        try:
            module_directory = module_path
            module_file = os.path.split(module_directory)[1]
            module_directory = module_directory.replace('/', '.')
            module_object = __import__(module_directory)
            module_object = self.get_module(module_object, module_file, module_directory)
            module_object = module_object.ZetaSploitModule()
        except:
            raise self.exceptions.GlobalException
        return module_object
    
    def import_plugin(self, plugin_path):
        try:
            plugin_directory = plugin_path
            plugin_file = os.path.split(plugin_directory)[1]
            plugin_directory = plugin_directory.replace('/', '.')
            plugin_object = __import__(plugin_directory)
            plugin_object = self.get_module(plugin_object, plugin_file, plugin_directory)
            plugin_object = plugin_object.ZetaSploitPlugin()
        except:
            raise self.exceptions.GlobalException
        return plugin_object
        
    def import_commands(self):
        commands = dict()
        command_path = self.config.path_config['base_paths']['commands_path']
        for menu in os.listdir(command_path):
            commands[menu] = dict()
        try:
            for command_menu in os.listdir(command_path):
                command_path = self.config.path_config['base_paths']['commands_path'] + command_menu
                for path, sub, files in os.walk(command_path):
                    for file in files:
                        if file.endswith('py'):
                            command_file_path = path + '/' + file[:-3]
                            try:
                                command_directory = command_file_path.replace(self.config.path_config['base_paths']['root_path'], '', 1)
                                command_object = self.import_command(command_directory)
                                command_name = command_object.details['Name']
                                commands[command_menu][command_name] = command_object
                            except:
                                self.badges.output_error("Failed to load " + file[:-3] + " command!")
                                sys.exit(1)
        except:
            self.badges.output_error("Failed to load console commands!")
            sys.exit(1)
        self.storage.set("commands", commands)

    def import_all(self):
        self.import_commands()
        self.db.add_modules(self.config.path_config['base_paths']['db_path'] + self.config.db_config['base_dbs']['modules_database'])
        self.db.add_plugins(self.config.path_config['base_paths']['db_path'] + self.config.db_config['base_dbs']['plugins_database'])
