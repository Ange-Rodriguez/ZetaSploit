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

from core.badges import badges
from core.helper import helper

class ZetaSploitPlugin:
    def __init__(self, controller):
        self.controller = controller
        self.badges = badges()
        self.helper = helper()

        self.details = {
            'Name':        "multi/trolling/say",
            'Authors':     ['enty8080'],
            'Description': "Say text message on device.",
            'Comment':     "idk?"
        }

        self.options = {
            'MESSAGE': {
                'Description': "Message to say.",
                'Value':       "Hello, zeterpreter!",
                'Required':    True
            }
        }

    def run(self):
        status, output = self.controller.send_command("say", self.options['MESSAGE']['Value'])
        if status == "error":
            self.helper.output(self.badges.E + "Failed to say message!")
