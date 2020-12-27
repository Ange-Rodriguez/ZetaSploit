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
import signal
import threading
import ctypes

from core.exceptions import exceptions
from core.formatter import formatter
from core.badges import badges
from core.storage import storage
from core.io import io
from core.modules import modules

class jobs():
    def __init__(self):
        self.exceptions = exceptions()
        self.formatter = formatter()
        self.badges = badges()
        self.storage = storage()
        self.io = io()
        self.modules = modules()

        self.job_process = None

    def check_jobs(self):
        if not self.storage.get("jobs"):
            return True
        return False

    def exit_jobs(self):
        if self.check_jobs():
            return True
        else:
            self.badges.output_warning("You have some running jobs.")
            state = self.badges.input_confirm("Exit anyway? [y/N] ").lower()
            if state  == "y" or state == "yes":
                self.badges.output_process("Stopping all jobs...")
                self.stop_all_jobs()
                return True
        return False

    def stop_all_jobs(self):
        if not self.check_jobs():
            for job_id in list(self.storage.get("jobs").keys()):
                self.delete_job(job_id)

    def stop_job(self, job):
        thread = job
        if not thread.is_alive():
            raise self.exceptions.GlobalException
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise self.exceptions.GlobalException
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise self.exceptions.GlobalException

    def start_job(self, job_function, job_arguments):
        self.job_process = threading.Thread(target=job_function, args=job_arguments)
        self.job_process.setDaemon(False)
        self.job_process.start()

    def delete_job(self, job_id):
        if not self.check_jobs():
            job_id = int(job_id)
            if job_id in list(self.storage.get("jobs").keys()):
                try:
                    self.stop_job(self.storage.get("jobs")[job_id]['job_process'])
                except:
                    pass
                try:
                    if self.storage.get("jobs")[job_id]['has_end_function']:
                        if self.storage.get("jobs")[job_id]['has_end_arguments']:
                            self.storage.get("jobs")[job_id]['end_function'](*self.storage.get("jobs")[job_id]['end_arguments'])
                        else:
                            self.storage.get("jobs")[job_id]['end_function']()
                except:
                    self.badges.output_error("Failed to stop job!")
                self.storage.delete_element("jobs", job_id)
            else:
                self.badges.output_error("Invalid job id!")
                raise self.exceptions.GlobalException
        else:
            self.badges.output_error("Invalid job id!")

    def create_job(self, job_name, module_name, job_function, job_arguments, end_function=None, end_arguments=None):
        self.start_job(job_function, job_arguments)
        job_end_function, job_end_arguments = True, True
        if not end_function:
            job_end_function = False
        if not end_arguments:
            job_end_arguments = False
        if not self.storage.get("jobs"):
            job_id = 0
            job_data = {
                job_id: {
                    'job_name': job_name,
                    'module_name': module_name,
                    'job_process': self.job_process,
                    'has_end_function': job_end_function,
                    'has_end_arguments': job_end_arguments,
                    'end_function': end_function,
                    'end_arguments': end_arguments
                }
            }
            self.storage.set("jobs", job_data)
        else:
            job_id = len(self.storage.get("jobs"))
            job_data = {
                job_id: {
                    'job_name': job_name,
                    'module_name': module_name,
                    'job_process': self.job_process,
                    'has_end_function': job_end_function,
                    'has_end_arguments': job_end_arguments,
                    'end_function': end_function,
                    'end_arguments': end_arguments
                }
            }
            self.storage.update("jobs", job_data)
        return job_id