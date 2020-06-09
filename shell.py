import chePibe


while True:
    inputText = input("CheLang >")
    result, error = chePibe.run("<stdin>",inputText)

    if error: print(error.as_string())
    else: print(result)