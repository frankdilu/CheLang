import cheLang
import signal
import sys

def signal_handler(sig, frame):
    print('Nos vemos wachin! Aguante Argentina!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    inputText = input("CheLang > ")

    result, error = cheLang.run("<stdin>",inputText)

    if error: print(error.as_string())
    elif result: print(repr(result))