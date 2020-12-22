#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020 EntySec
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
import sys
import re

from core.badges import badges
from core.exceptions import exceptions
from core.io import io
from core.jobs import jobs
from core.storage import storage

class main:
    def __init__(self):
        self.badges = badges()
        self.exceptions = exceptions()
        self.io = io()
        self.jobs = jobs()
        self.storage = storage()

    def main_menu(self):
        while True:
            try:
                commands, arguments = self.io.input('(zsf)> ')
                if commands == []:
                    continue
                else:
                    if commands[0] in self.storage.get("commands")['main'].keys():
                        command = self.storage.get("commands")['main'][commands[0]]
                        if command.details['NeedsArgs']:
                            if (len(commands) - 1) < command.details['ArgsCount']:
                                self.io.output("Usage: " + command.details['Usage'])
                            else:
                                arguments = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', arguments)
                                formated_args = []
                                for i in arguments:
                                    formated_args.append(i.strip('"' and "'"))
                                command.details['Args'] = formated_args
                                try:
                                    command.run()
                                except (KeyboardInterrupt, EOFError):
                                    self.io.output("")
                        else:
                            try:
                                command.run()
                            except (KeyboardInterrupt, EOFError):
                                self.io.output("")
                    else:
                        found = True
                        if self.storage.get("loaded_plugins"):
                            for plugin in self.storage.get("loaded_plugins").keys():
                                if hasattr(self.storage.get("loaded_plugins")[plugin], "commands"):
                                    if commands[0] in self.storage.get("loaded_plugins")[plugin].commands.keys():
                                        command = self.storage.get("loaded_plugins")[plugin].commands[commands[0]]
                                        if command['NeedsArgs']:
                                            if (len(commands) - 1) < command['ArgsCount']:
                                                self.io.output("Usage: " + command['Usage'])
                                            else:
                                                arguments = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', arguments)
                                                formated_args = []
                                                for i in arguments:
                                                    formated_args.append(i.strip('"' and "'"))
                                                command['Args'] = formated_args
                                                try:
                                                    command['Run']()
                                                except (KeyboardInterrupt, EOFError):
                                                    self.io.output("")
                                        else:
                                            try:
                                                command['Run']()
                                            except (KeyboardInterrupt, EOFError):
                                                self.io.output("")
                                    else:
                                        found = False
                                else:
                                    found = False
                        else:
                            found = False
                        if not found:
                            self.badges.output_error("Unrecognized command!")

            except (KeyboardInterrupt, EOFError):
                self.io.output("")
            except self.exceptions.ExitMenuException:
                break
            except Exception as e:
                self.badges.output_error("An error occurred: " + str(e) + "!")