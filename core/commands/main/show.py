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
from core.badges import badges
from core.storage import storage
from core.modules import modules
from core.formatter import formatter

class ZetaSploitCommand:
    def __init__(self):
        self.io = io()
        self.badges = badges()
        self.storage = storage()
        self.modules = modules()
        self.formatter = formatter()

        self.details = {
            'Label': "core",
            'Name': "show",
            'Description': "Show specified information.",
            'Usage': "show <information>",
            'ArgsCount': 1,
            'NeedsArgs': True,
            'Args': list()
        }

    def run(self):
        information = self.details['Args'][0]
        modules = self.storage.get("modules")
        usage = "Informations: "
        for category in sorted(modules.keys()):
            usage += category + ", "
        usage += "plugins"
        if information in modules.keys():
            modules_data = list()
            headers = ("Name", "Description")
            modules = modules[information]
            for platform in sorted(modules.keys()):
                for module in sorted(modules[platform].keys()):
                    full_name = self.modules.get_full_name(information, platform, module)
                    modules_data.append((full_name, modules[platform][module]['Description']))
            self.io.output("")
            self.formatter.format_table("Modules", headers, *modules_data)
            self.io.output("")
        else:
            if information == "plugins":
                if self.storage.get("plugins"):
                    plugins_data = list()
                    headers = ("Name", "Description")
                    plugins = self.storage.get("plugins")
                    for plugin in sorted(plugins.keys()):
                        plugins_data.append((plugin, plugins[plugin]['Description']))
                    self.io.output("")
                    self.formatter.format_table("Plugins", headers, *plugins_data)
                    self.io.output("")
                else:
                    self.badges.output_warning("No plugins available!")
            else:
                self.badges.output_information(usage)
