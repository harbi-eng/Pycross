# Pycross
---

Pycross is a python module for handling cross intrepreters communcation.

# About
---

The Pycross module provides a set of python decorators to be used in order to interpret functions on another python interpreter, the communication between these python interpreters uses ethier a sharedmemory module for inter-process communication(IPC), and the Net module is used to make the communication between Remote processes.


by this project you can for example use python 2.7 interpreter with python 3.x interpreter to work in the same program, or use IronPython, Jython, PyPy, and CPython interpreters to work in the same project, you can asign each one of these interpreteres or others a function, and let each one of them excute it, and you will get the result, the way of asigning the functions to the required interpreter is made by seting the path of the interpreter first, then use that intrpreter decorator, there are alos some examples to demonstrat how to use Pycross.

 Compatibility problems
---

to be able to use the shared memory module, you have use a posix operating system such as linux, the shared memory won't work in windows or macOS, also you you can only use it with CPython and PyPy, becasue of the C-extensions supports in these two interpreters, if you want to use the project with another interprters or in another operating system such as windows or macOS, you can use the Net Module to handle the communication between the interpreters.




