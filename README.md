py-cpuutilization
=================

[![Downloads](https://pypip.in/d/py-cpuutilization/badge.png?period=month)](https://pypi.python.org/pypi/py-cpuutilization/)
[![Latest Version](https://pypip.in/v/py-cpuutilization/badge.png)](https://pypi.python.org/pypi/py-cpuutilization/)
[![License](https://pypip.in/license/py-cpuutilization/badge.png)](https://pypi.python.org/pypi/py-cpuutilization/)

A module for getting the CPU utilization on any OS with Python 2 & 3

Py-cpuutilization should work without any extra programs or libraries, beyond 
what your OS provides. The goal is for this to work on every OS that Python 
supports. Works on Linux, OS X, Windows, BSD, Solaris, Cygwin, and Haiku.

Run as a script
-----

    from cpuutilization import cpuutilization
    print(cpuutilization.get_utilization())

