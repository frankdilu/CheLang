import signal
import sys
import os
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("CheLang Shell")

from CheLang.cheLangCompiler import run  
from CheLang.Values import Empty

def signal_handler(sig, frame):
    print('Nos vemos wachin! Aguante Argentina!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if len(sys.argv) == 1:
    while True:
        inputText = input("CheLang > ")
        if inputText.strip() == "": continue
        result, error = run(__file__,inputText)

        if error: print(error.as_string())

        elif result: 

            for i,r in enumerate(result.elements):
                if type(r) == Empty:
                    result.elements.pop(i)

            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            elif len(result.elements) > 1:
                print(repr(result))
else:
    uri = sys.argv[1].replace("\\","\\\\")
    result, error = run(__file__, f'run("{uri}")')

    if error: print(error.as_string())

    elif result: 

        for i,r in enumerate(result.elements):
            if type(r) == Empty:
                result.elements.pop(i)

        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        elif len(result.elements) > 1:
            print(repr(result))
    input("CheLang > Apreta enter pa cerrar eto")
    sys.exit(0)