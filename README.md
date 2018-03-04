py-cpuutilization
=================

 &nbsp;
 
 &nbsp;


:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:

:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:

!!! WARNING !!!
=========

As of September 2017, this project is deprecated.


 
 :warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
 :warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
 :warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:

:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:
 
 &nbsp;
 
 &nbsp;
 
 &nbsp;
 
 &nbsp;

[![Latest Version](https://img.shields.io/pypi/v/py-cpuutilization.svg)](https://pypi.python.org/pypi/py-cpuutilization/)
[![License](https://img.shields.io/pypi/l/py-cpuutilization.svg)](https://pypi.python.org/pypi/py-cpuutilization/)

A module for getting the CPU utilization on any OS with Python 2 & 3

Py-cpuutilization should work without any extra programs or libraries, beyond 
what your OS provides. The goal is for this to work on every OS that Python 
supports. Works on Linux, OS X, Windows, BSD, Solaris, Cygwin, and Haiku.

Run as a script
-----

~~~python
    from cpuutilization import cpuutilization
    print(cpuutilization.get_utilization())
~~~
