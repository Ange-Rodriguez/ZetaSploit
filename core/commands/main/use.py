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

import os

from core.io import io
from core.menus.module import module
from core.importer import importer
from core.badges import badges
from core.storage import storage
from core.modules import modules

class ZetaSploitCommand:
    def __init__(self):
        self.io = io()
        self.module = module()
        self.importer = importer()
        self.badges = badges()
        self.storage = storage()
        self.modules = modules()

        self.details = {
            'Name': "use",
            'Description': "Use specified module.",
            'Usage': "use <module>",
            'ArgsCount': 1,
            'NeedsArgs': True,
            'Args': list()
        }
        
    def import_module(self, module):
        modules = self.storage.get("modules")
        try:
            module_object = self.importer.import_module(modules[category][module]['Path'])
            if not self.storage.get("imported_modules"):
                self.storage.set("imported_modules", list())
            self.storage.append("imported_modules", module)
        except:
            return False
        return True
        
    def add_module(self, module):
        modules = self.storage.get("modules")
        not_installed = list()
        for dependence in modules[category][module]['Dependencies']:
            if not self.importer.import_check(dependence):
                not_installed.append(dependence)
        if not not_installed:
            imported_modules = self.storage.get("imported_modules")
            if not imported_modules or module not in imported_modules:
                if not self.import_module(module):
                    return
            self.storage.set("current_module", [])
            self.storage.set("pwd", 0)
            self.storage.add_array("current_module", '')
            self.storage.set_array("current_module", self.storage.get("pwd"), module_object)
            self.module.module_menu()
        else:
            self.badges.output_error("Module depends this dependencies which is not installed:")
            for dependence in not_installed:
                self.io.output("    " + dependence)

    def run(self):
        module = self.details['Args'][0]
        modules = self.storage.get("modules")
        category = self.modules.get_category(module)
        if category in modules.keys():
            module = self.modules.get_name(module)
            if module in modules[category].keys():
                self.add_module(module)
            else:
                self.badges.output_error("Invalid module!")
        else:
            self.badges.output_error("Invalid module!")
