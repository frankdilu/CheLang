import cheLang
import signal
import sys

if len(sys.argv) == 1:
    def signal_handler(sig, frame):
        print('Nos vemos wachin! Aguante Argentina!')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        inputText = input("CheLang > ")
        if inputText.strip() == "": continue
        result, error = cheLang.run(__file__,inputText)

        if error: print(error.as_string())
        elif result: 
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
else:
    result, error = cheLang.run(__file__, f'run("{sys.argv[1]}")')
    if error: print(error.as_string())
    elif result: 
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))