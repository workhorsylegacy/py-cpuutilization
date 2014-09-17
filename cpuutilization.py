#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2014, Matthew Brennan Jones <matthew.brennan.jones@gmail.com>
# A module for getting the CPU utilization on any OS with Python 2 & 3
# It uses a MIT style license
# It is hosted at: https://github.com/workhorsy/py-cpuutilization
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import platform
import subprocess


PY2 = sys.version_info[0] == 2

def _chomp(s):
	for sep in ['\r\n', '\n', '\r']:
		if s.endswith(sep):
			return s[:-len(sep)]

	return s

class _ProcessRunner(object):
	def __init__(self, command):
		self._command = command
		self._process = None
		self._return_code = None
		self._stdout = None
		self._stderr = None

	def run(self):
		self._stdout = []
		self._stderr = []

		# Start the process and save the output
		self._process = subprocess.Popen(
			self._command,
			stderr = subprocess.PIPE,
			stdout = subprocess.PIPE,
			shell = True
		)

	def wait(self):
		# Wait for the process to actually exit
		self._process.wait()

		# Get the return code
		rc = self._process.returncode
		if hasattr(os, 'WIFEXITED') and os.WIFEXITED(rc):
			rc = os.WEXITSTATUS(rc)
		self._return_code = rc

		# Get strerr and stdout into byte strings
		self._stderr = b''.join(self._stderr)
		self._stdout = b''.join(self._stdout)

		# Convert strerr and stdout into unicode
		if PY2:
			self._stderr = unicode(self._stderr, 'UTF-8')
			self._stdout = unicode(self._stdout, 'UTF-8')
		else:
			self._stderr = str(self._stderr, 'UTF-8')
			self._stdout = str(self._stdout, 'UTF-8')

		# Chomp the terminating newline off the ends of output
		self._stdout = _chomp(self._stdout)
		self._stderr = _chomp(self._stderr)

	def get_is_done(self):
		# You have to poll a process to update the retval. Even if it has stopped already
		if self._process.returncode == None:
			self._process.poll()

		# Read the output from the buffer
		sout, serr = self._process.communicate()
		self._stdout.append(sout)
		self._stderr.append(serr)

		# Return true if there is a return code
		return self._process.returncode != None
	is_done = property(get_is_done)

	def get_stderr(self):
		self._require_wait()
		return self._stderr
	stderr = property(get_stderr)

	def get_stdout(self):
		self._require_wait()
		return self._stdout
	stdout = property(get_stdout)

	def get_stdall(self):
		self._require_wait()
		return self._stdout + '\n' + self._stderr
	stdall = property(get_stdall)

	def get_is_success(self):
		self._require_wait()
		return self._return_code == 0
	is_success = property(get_is_success)

	def _require_wait(self):
		if self._return_code == None:
			raise Exception("Wait needs to be called before any info on the process can be gotten.")

def _run_and_get_stdout(command):
	runner = _ProcessRunner(command)
	runner.run()
	runner.is_done
	runner.wait()
	if runner.is_success:
		return runner.stdout
	else:
		return None

def get_utilization():
	# Figure out the general OS type
	uname = platform.system().lower().strip()

	if 'linux' in uname or 'cygwin' in uname:
		command = 'top -b -n 2 -d 1'
		out = _run_and_get_stdout(command)

		# Get the cpu percentages
		out = out.split("%Cpu(s):")[2]
		out = out.split('\n')[0]
		out = out.split(',')

		# Add the percentages to get the real cpu usage
		speed = \
		float(out[0].split('us')[0]) + \
		float(out[1].split('sy')[0]) + \
		float(out[2].split('ni')[0])

		return speed
	elif 'bsd' in uname:
		command = 'top -b -P -s 2 -d 2'
		out = _run_and_get_stdout(command)

		# Get the cpu percentages
		out = out.split("CPU:")[1]
		out = out.split('\n')[0]
		out = out.split(',')

		# Add the percentages to get the real cpu usage
		speed = \
		float(out[0].split('% user')[0]) + \
		float(out[1].split('% nice')[0]) + \
		float(out[2].split('% system')[0])

		return speed
	elif 'darwin' in uname:
		command = 'top -F -l 2 -i 2 -n 0'
		out = _run_and_get_stdout(command)

		# Get the cpu percentages
		out = out.split("CPU usage:")[2]
		out = out.split('\n')[0]
		out = out.split(',')

		# Add the percentages to get the real cpu usage
		speed = \
		float(out[0].split('% user')[0]) + \
		float(out[1].split('% sys')[0])

		return speed
	elif 'solaris' in uname or 'sunos' in uname:
		command = 'top -b -s 2 -d 2'
		out = _run_and_get_stdout(command)

		# Get the cpu percentages
		out = out.split("CPU states: ")[2]
		out = out.split('\n')[0]
		out = out.split(',')

		# Add the percentages to get the real cpu usage
		speed = \
		float(out[1].split('% user')[0]) + \
		float(out[2].split('% kernel')[0]) + \
		float(out[3].split('% iowait')[0])

		return speed
	elif 'beos' in uname or 'haiku' in uname:
		command = 'top -d -i 2 -n 2'
		out = _run_and_get_stdout(command)

		# Get the cpu percentages
		out = out.split("------")[1]
		out = out.split('% TOTAL')[0]
		out = out.split()

		# Add the percentages to get the real cpu usage
		speed = float(out[-1])

		return speed
	elif 'windows' in uname:
		command = 'wmic cpu get loadpercentage'
		out = _run_and_get_stdout(command)

		# Get the cpu percentages
		out = out.split()[-1]

		# Add the percentages to get the real cpu usage
		speed = float(out)

		return speed


if __name__ == '__main__':
	print(get_utilization())





