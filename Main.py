from brain import brain


def main():
    print("Welcome to the c0 compiler:")
    compiler = brain()
    text = ""
    while text!="exit":
        text = input("-->")
        if text=="exit":
            print("Bye")
            break
        if not "=" in text:
            try:
                print(brain.operator(text))
            except:
                print("Error! Invalid Syntax")
        if "=" in text:
            try:
                compiler.setValue(text)
            except:
                print("Error! Invalid Syntax")
        if text=="print vars":
            try:
                print("madeit")
                compiler.printVars()
            except:
                print("No variables to print")
        if text in compiler.vars:
            compiler.getValue(text)
        if "for" in text or "while" in text or "if" in text:
            compiler.loops(text)
        if brain.isComparison(text):
            compiler.setValue(text)
        if "print" in text:
            compiler.setValue(text)
        if brain.containsFunction(text):
            compiler.getFunctionName(text)
            print(compiler.functionName)
            compiler.storeParameters(text,compiler.functionName)
            #for i in range(len(text[text.find("(")+1:text.find(")")].split(","))):
            #    compiler.funcs[compiler.functionName][1][i] = text[text.find("(")+1:text.find(")")].split(",")[i]
            while compiler.isFunction:
                text = input("...")
                if text == "}":
                    print("Bye!")
                    compiler.isFunction = False
                else:
                    compiler.functionStoreValue(text,compiler.functionName)
        if compiler.functionCall(text):
            print("function call")
            text = brain.removeSpaces(text)
            compiler.functionCalled = True
            print("commands",compiler.funcs[compiler.functionName])
            #compiler.storeParameters(text,compiler.functionName)
            #for i in range(len(text[text.find("(")+1:text.find(")")].split(","))):
            #    compiler.funcs[compiler.functionName][1][i] = text[text.find("(")+1:text.find(")")].split(",")[i]
            counter = 0
            for var in compiler.funcs[compiler.functionName][1]:
                if isinstance(compiler.funcs[compiler.functionName][1][var],str):
                    compiler.funcs[compiler.functionName][1][var] = text[text.find("(")+1:text.find(")")].split(",")[counter]
                elif isinstance(compiler.funcs[compiler.functionName][1][var],int):
                    compiler.funcs[compiler.functionName][1][var] = int(text[text.find("(")+1:text.find(")")].split(",")[counter])
                elif text[text.find("(")+1:text.find(")")].split(",")[counter] == "true":
                    compiler.funcs[compiler.functionName][1][var] = True
                elif text[text.find("(")+1:text.find(")")].split(",")[i] == "false":
                    compiler.funcs[compiler.functionName][1][var] = False
                counter+=1
            for command in compiler.funcs[compiler.functionName][0]:
                if not "=" in command:
                    try:
                        print(brain.operator(command))
                    except:
                        print("Error! Invalid Syntax")
                if "=" in command:
                    try:
                        compiler.functionSetValue(command,compiler.functionName)
                    except:
                        print("Error! Invalid Syntax")
                if command=="print vars":
                    try:
                        print("madeit")
                        compiler.functionPrintVars(compiler.functionName)
                    except:
                        print("No variables to print")
                if command in compiler.funcs[compiler.functionName][1]:
                    try:
                        compiler.functionGetValue(command,compiler.functionName)
                    except:
                        print("Error! Invalid syntax")
                if "for" in command or "while" in command or "if" in command:
                    print("loopy")
                    try:
                        compiler.loops(command)
                    except:
                        print("Error! Invalid syntax")
                print("Bands a make her dance")
                if brain.isComparison(command):
                    print("Scheisce")
                    compiler.functionSetValue(command,compiler.functionName)
                if (not "for" in command and not "while" in command and not "if" in command) and "print" in command:
                    print("shit")
                    compiler.functionSetValue(command,compiler.functionName)
                if "return" in command:
                    command = brain.removeSpaces(command)
                    if command[command.find("return")+6:] in compiler.funcs[compiler.functionName][1]:
                        compiler.funcs[compiler.functionName][1]["return"] = compiler.funcs[compiler.functionName][1][command[command.find("return")+6:]]
                    else:
                        try:
                            compiler.funcs[compiler.functionName][1]["return"] = int(command[command.find("return")+6:])
                        except:
                            if command[command.find("return")+6:] == "true":
                                compiler.funcs[compiler.functionName][1]["return"] = True
                            elif command[command.find("return")+6:] == "false":
                                compiler.funcs[compiler.functionName][1]["return"] = False
                            else:
                                compiler.funcs[compiler.functionName][1]["return"] = command[command.find("return")+6:]
                print("changes",compiler.funcs[compiler.functionName][1])
        if compiler.setFuncValue(text):
            print("I am setting the value of a program variable to the return of a function")
            text = brain.removeSpaces(text)
            compiler.functionCalled = True
            print("commands",compiler.funcs[compiler.functionName])
            #compiler.storeParameters(text,compiler.functionName)
            #for i in range(len(text[text.find("(")+1:text.find(")")].split(","))):
            #    compiler.funcs[compiler.functionName][1][i] = text[text.find("(")+1:text.find(")")].split(",")[i]
            counter = 0
            for var in compiler.funcs[compiler.functionName][1]:
                if isinstance(compiler.funcs[compiler.functionName][1][var],str):
                    compiler.funcs[compiler.functionName][1][var] = text[text.find("(")+1:text.find(")")].split(",")[counter]
                elif isinstance(compiler.funcs[compiler.functionName][1][var],int):
                    compiler.funcs[compiler.functionName][1][var] = int(text[text.find("(")+1:text.find(")")].split(",")[counter])
                elif text[text.find("(")+1:text.find(")")].split(",")[counter] == "true":
                    compiler.funcs[compiler.functionName][1][var] = True
                elif text[text.find("(")+1:text.find(")")].split(",")[i] == "false":
                    compiler.funcs[compiler.functionName][1][var] = False
                counter+=1
            for command in compiler.funcs[compiler.functionName][0]:
                if not "=" in command:
                    try:
                        print(brain.operator(command))
                    except:
                        print("Error! Invalid Syntax")
                if "=" in command:
                    try:
                        compiler.functionSetValue(command,compiler.functionName)
                    except:
                        print("Error! Invalid Syntax")
                if command=="print vars":
                    try:
                        print("madeit")
                        compiler.functionPrintVars(compiler.functionName)
                    except:
                        print("No variables to print")
                if command in compiler.funcs[compiler.functionName][1]:
                    try:
                        compiler.functionGetValue(command,compiler.functionName)
                    except:
                        print("Error! Invalid syntax")
                if "for" in command or "while" in command or "if" in command:
                    print("loopy")
                    try:
                        compiler.loops(command)
                    except:
                        print("Error! Invalid syntax")
                print("Bands a make her dance")
                if brain.isComparison(command):
                    print("Scheisce")
                    compiler.functionSetValue(command,compiler.functionName)
                if (not "for" in command and not "while" in command and not "if" in command) and "print" in command:
                    print("shit")
                    compiler.functionSetValue(command,compiler.functionName)
                if "return" in command:
                    command = brain.removeSpaces(command)
                    if command[command.find("return")+6:] in compiler.funcs[compiler.functionName][1]:
                        compiler.funcs[compiler.functionName][1]["return"] = compiler.funcs[compiler.functionName][1][command[command.find("return")+6:]]
                    else:
                        try:
                            compiler.funcs[compiler.functionName][1]["return"] = int(command[command.find("return")+6:])
                        except:
                            if command[command.find("return")+6:] == "true":
                                compiler.funcs[compiler.functionName][1]["return"] = True
                            elif command[command.find("return")+6:] == "false":
                                compiler.funcs[compiler.functionName][1]["return"] = False
                            else:
                                compiler.funcs[compiler.functionName][1]["return"] = command[command.find("return")+6:]
                print("changes",compiler.funcs[compiler.functionName][1])
            compiler.functionSetValue(text,compiler.functionName)
    



main()