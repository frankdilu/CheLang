import cheLang


while True:
    inputText = input("CheLang >")
    result, error = cheLang.run("<stdin>",inputText)

    if error: print(error.as_string())
    else: print(result)