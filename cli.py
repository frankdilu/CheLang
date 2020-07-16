import signal
import sys
import os
import ctypes
import datetime
try:
    # name of console
    ctypes.windll.kernel32.SetConsoleTitleW("Consola CheLang")
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


def cli():
    # sacamo los argumentos opcionales
    for arg in sys.argv:
        if arg[0] == "-":
            sys.argv.remove(arg)
    # if 1 argument open console
    if len(sys.argv) == 1:
        while True:
            folder = os.path.basename(os.getcwd())
            inputText = input("/"+ folder + " < CheLang > ")
            inputText = inputText.replace("\\","\\\\")
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
        uri = sys.argv[1]
        uri = uri.replace("\\","\\\\")
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

now = datetime.datetime.now()
#Los feriado mas importantes vistes
feriados = [
    "1.1","24.2","25.2","23.3",
    "24.3","31.3","10.4","1.5",
    "25.5","15.6","20.6","9.7",
    "10.7","17.8","12.10","23.11",
    "7.12","8.12","25.12"
    ]

#Si no es finde o estan los milicos se trabaja siempre
if now.weekday() < 5 and not (str(now.day) + "." + str(now.month)) in feriados:
    cli()
elif "--milicos" in sys.argv:
    print("\n*Videla happy noises*\n")
    cli()

print("No hermano, fin de semana o feriado en Argentina no se trabaja.")
input("\nApreta enter, dale.\n")
sys.exit(0)