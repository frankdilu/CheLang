import signal
import sys
import os
import ctypes
try:
    # name of console
    ctypes.windll.kernel32.SetConsoleTitleW("CheLang Shell")
except:
    pass

from CheLang.cheLangCompiler import run  
from CheLang.Values import Empty

# ctrl + c function
def signal_handler(sig, frame):
    print('Nos vemos wachin! Aguante Argentina!')
    sys.exit(0)

# set ctrl + c function
signal.signal(signal.SIGINT, signal_handler)


# if 1 argument open console
if len(sys.argv) == 1:
    while True:
        folder = os.path.basename(os.getcwd())
        inputText = input("/"+ folder + " < CheLang > ")
        if inputText.strip() == "": continue
        result, error = run(__file__,inputText)

        if error: print(error.as_string())

        elif result: 
            # sacanding los Empty
            for i,r in enumerate(result.elements):
                if type(r) == Empty:
                    result.elements.pop(i)

            for programReturn in result.elements:
                print(repr(programReturn))
# if 2 argument open file
else:
    uri = sys.argv[1].replace("\\","\\\\")
    result, error = run(__file__, f'Correme("{uri}")')

    if error: print(error.as_string())

    elif result: 

        # sacanding los Empty
        for i,r in enumerate(result.elements):
            if type(r) == Empty:
                result.elements.pop(i)

        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        elif len(result.elements) > 1:
            print(repr(result))
    folder = os.path.basename(os.getcwd())
    input("/"+ folder + " CheLang > Apreta enter pa cerrar eto")
    sys.exit(0)