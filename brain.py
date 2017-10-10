#c0 interpreter in python

class brain(object):
    def __init__(self):
        #self.input = input.split(";")
        self.vars = dict()  #Variables not in functions
        self.funcs = dict()  #Tuple of function and dicionary with in-line function(lambda) and dictionary of local function variables
        self.functionName = ""
        self.isFunction = False
        self.functionCalled = False

    Contracts = set()
    Contracts.add("requires")
    Contracts.add("ensures")
    Contracts.add("loop_invariant")
    Contracts.add("assert")

    Boolean = dict()
    Boolean["true"] = True
    Boolean["false"] = False


    @staticmethod
    def removeSpaces(command):
        newCommand = ""
        for i in range(len(command)):
            if ord(command[i])!=32:
                newCommand+=command[i]
        return newCommand


    @staticmethod
    def containsInt(command):  #Checks to see if a given command contains an int
        command = brain.removeSpaces(command)
        try:
            x = int(command[command.find("=")+1:])
            if "=" in command and command[0:3] == "int":
                return True
            else:
                print("ewwwwwwww")
                print("Error! Invalid syntax")
                return False
        except:
            print("Error! Invalid syntax")
            return False
    @staticmethod
    def operator(command):
        command = brain.removeSpaces(command)
        #print(command)
        if "*" in command:
            v1 = int(command[:command.find("*")])
            v2 = int(command[command.find("*")+1:])
            return v1*v2
        elif "/" in command:
            v1 = int(command[:command.find("/")])
            v2 = int(command[command.find("/")+1:])
            return v1/v2
        elif "<<" in command:
            v1 = int(command[:command.find("<<")])
            v2 = int(command[command.find("<<")+2:])
            return v1*(2**v2)
        elif ">>" in command:
            v1 = int(command[:command.find(">>")])
            v2 = int(command[command.find(">>")+2:])
            return v1/(2**v2)
        elif "+" in command:
            v1 = int(command[:command.find("+"):])
            v2 = int(command[command.find("+")+1:])
            return v1+v2
        elif "-" in command:
            v1 = int(command[:command.find("-"):])
            v2 = int(command[command.find("-")+1:])
            return v1-v2

    @staticmethod
    def isComparison(command):
        command = brain.removeSpaces(command)
        return "&&" in command or "^" in command or "||" in command

    @staticmethod
    def comparisons(command):
        command = brain.removeSpaces(command)
        if "&&" in command:
            v1 = command[:command.find("&&")]
            v2 = command[command.find("&&")+2:]
            return v1 and v2
        elif "^" in command:
            v1 = command[:command.find("^")]
            v2 = command[command.find("^")+1:]
            if v1 and v2:
                return False
            elif not v1 and not v2:
                return False
            else:
                return True
        elif "||" in command:
            v1 = command[:command.find("||")]
            v2 = command[command.find("||")+2:]
            return v1 or v2


    @staticmethod
    def isComment(command):
        if command[:2]=="/*":
            if command[-2:]=="*/":
                return True
            else:
                return "Error! Invalid syntax"
        return False

    @staticmethod
    def isContract(command):
        command = brain.removeSpaces(command)
        for contract in brain.Contracts:
            if contract in command:
                return command[:3]=="//@"
        return False

    @staticmethod
    def printStatement(command):
        return "print(" in command

    @staticmethod
    def containsString(command):
        try:
            x = int(command[command.find("=")+1:])
            print("Error! Invalid syntax")
            return False
        except:
            return "=" in command and command[:6]=="string" and len(command[command.find("=")+1:])>1 and not "[]" in command

    @staticmethod
    def containsChar(command):
        command = brain.removeSpaces(command)
        try:
            x = int(command[command.find("=")+1:])
            print("Error! Invalid syntax")
            return False
        except:
            return "=" in command and command[:4]=="char" and len(command[command.find("=")+1:])==1

    @staticmethod
    def containsBool(command):
        command = brain.removeSpaces(command)
        return command[:4]=="bool" and command[command.find("=")+1:]=="true" or command[command.find("=")+1:]=="false"

    @staticmethod
    def containsArray(command):  #int[] = alloc_array(int,10)
        command = brain.removeSpaces(command)
        if command[:5] == "int[]" and command[command.find("=")+1:command.find("(")] == "alloc_array":
            return True
        elif command[:8] == "string[]" and command[command.find("=")+1:command.find("(")] == "alloc_array":
            return True
        elif command[:6] == "char[]" or command[:6] == "bool[]" and command[command.find("=")+1:command.find("(")] == "alloc_array":
            return True
        return False


    @staticmethod
    def updateValue(command):
        command = brain.removeSpaces(command)
        return command[command.find("=")-1] in "*/-+"

    @staticmethod
    def containsFunction(command):
        command = brain.removeSpaces(command)
        #print(command)
        print(command[:3]=="int" and "(" in command and ")" in command and "{" in command)
        if command == "exit":
            return False
        if command[:3]=="int" and "(" in command and ")" in command and "{" in command:
            return True
        elif command[:6]=="string" and "(" in command and ")" in command and "{" in command:
            return True
        elif command[:4]=="bool" and "(" in command and ")" in command and "{" in command:
            return True
        elif command[:4]=="char" and "(" in command and ")" in command and "{" in command:
            return True
        elif command[:4] == "void" and "(" in command and ")" in command and "{" in command:
            return True
        return False

    def functionCall(self,command):  #Checks to see if a function is being called
        #return "=" in command and command[command.find("=")+1:command.find("(")] in self.funcs or not "=" in command and command[:command.find("(")] in self.funcs
        return command[:command.find("(")] in self.funcs

    def setFuncValue(self,command):
        command = brain.removeSpaces(command)
        return "=" in command and command[command.find("=")+1:command.find("(")] in self.funcs

    def setValue(self,command):
        command = brain.removeSpaces(command)
        print("command",command)
        print("bsbs",command[command.find("=")-1])
        if brain.containsInt(command):
            print("hello",command)
            command = brain.removeSpaces(command)
            var = ""
            var = command[3:command.find("=")]
            self.vars[var] = int(command[command.find("=")+1:])
            print(var+"="+str(self.vars[var]))
        elif brain.containsString(command):
            print("string")
            command = brain.removeSpaces(command)
            var = ""
            var = command[6:command.find("=")]
            self.vars[var] = command[command.find("=")+1:]
            print(var+"="+self.vars[var])
        elif brain.containsBool(command):
            print("bool")
            command = brain.removeSpaces(command)
            if command[-4:] == "true" and not brain.containsFunction(command):
                print("true")
                print(command[command.find("bool")+4:command.find("=")])
                self.vars[command[command.find("bool")+4:command.find("=")]] = True
                print("made it")
            elif "false" in command and not brain.containsFunction(command):
                self.vars[command[command.find("bool")+4:command.find("=")]] = False
            #Access boolean dictionary and then translate values to True or False
        elif brain.containsChar(command):
            print("char")
            command = brain.removeSpaces(command)
            var = ""
            var = command[4:command.find("=")]
            self.vars[var] = command[command.find("=")+1:]
            print(var+"="+self.vars[var])
        elif brain.isContract(command):
            pass
        elif brain.updateValue(command):
            command = brain.removeSpaces(command)
            print("sup",command)
            if isinstance(self.vars[command[command.find("=")-2]],int):  #Need to change, because strings can added to with +=
                if command[command.find("=")-1]=="*":
                    #print("key",command[:command.find("=")-1])
                    self.vars[command[:command.find("=")-1]]*=int(command[command.find("=")+1:])
                elif command[command.find("=")-1]=="/":
                    self.vars[command[:command.find("=")-1]]/=int(command[command.find("=")+1:])
                elif command[command.find("=")-1]=="+":
                    self.vars[command[:command.find("=")-1]]+=int(command[command.find("=")+1:])
                elif command[command.find("=")-1]=="-":
                    self.vars[command[:command.find("=")-1]]-=int(command[command.find("=")+1:])
            elif isinstance(self.vars[command[command.find("=")-2]],str):
                if command[command.find("=")-1]=="+":
                    self.vars[command[:command.find("=")-1]]+=command[command.find("=")+1:]
                else:
                    print("Error! Invalid syntax")
            else:
                print("Error! Invalid syntax")
        elif brain.printStatement(command):
            print(command[command.find("(")+1:command.find(")")])
        elif brain.isComparison(command):
            brain.comparison(command)
        elif brain.containsArray(command):
            command = brain.removeSpaces(command)
            try:
                if command[:3] == "int":
                    self.vars[command[command.find("]")+1:command.find("=")]] = [0 for row in range(int(command[command.find(",")+1:command.find(")")]))]
                elif command[:6] == "string":
                    self.vars[command[command.find("]")+1:command.find("=")]] = ["Hello" for row in range(int(command[command.find(",")+1:command.find(")")]))]
                elif command[:4] == "char":
                    self.vars[command[command.find("]")+1:command.find("=")]] = ["C" for row in range(int(command[command.find(",")+1:command.find(")")]))]
                elif command[:4] == "bool":
                    self.vars[command[command.find("]")+1:command.find("=")]] = [True for row in range(int(command[command.find(",")+1:command.find(")")]))]
            except:
                print("Error! Invalid syntax")

    def getFunctionName(self,command):
        command = brain.removeSpaces(command)
        lines = []
        if command[:3] == "int":
            self.functionName = command[3:command.find("(")]
            self.funcs[command[3:command.find("(")]] = ([],dict())
        elif command[:6] == "string":
            self.functionName = command[6:command.find("(")]
            self.funcs[command[6:command.find("(")]] = ([],dict())
        elif command[:4] == "char":
            self.functionName = command[4:command.find("(")]
            self.funcs[command[4:command.find("(")]] = ([],dict())
        elif command[:4] == "bool":
            self.functionName = command[4:command.find("(")]
            self.funcs[command[4:command.find("(")]] = ([],dict())
        elif command[:4] == "void":
            self.functionName = command[4:command.find("(")]
            self.funcs[command[4:command.find("(")]] = ([],dict())
        self.isFunction = True

    def functionSetValue(self,command,function):
        command = brain.removeSpaces(command)
        print("command",command)
        print("bsbs",command[command.find("=")-1])
        if brain.containsInt(command):
            print("hello",command)
            command = brain.removeSpaces(command)
            var = ""
            var = command[3:command.find("=")]
            self.funcs[function][1][var] = int(command[command.find("=")+1:])
            print("supppeprpererer",var+"="+str(self.funcs[function][1][var]))
        elif brain.containsString(command):
            print("string")
            command = brain.removeSpaces(command)
            var = ""
            var = command[6:command.find("=")]
            self.funcs[function][1][var] = command[command.find("=")+1:]
            print(var+"="+self.funcs[function][1][var])
        elif brain.containsBool(command):
            print("bool")
            command = brain.removeSpaces(command)
            if command[-4:] == "true" and not brain.containsFunction(command):
                print("true")
                print(command[command.find("bool")+4:command.find("=")])
                self.funcs[function][1][command[command.find("bool")+4:command.find("=")]] = True
                print("made it")
            elif "false" in command and not brain.containsFunction(command):
                self.funcs[function][1][command[command.find("bool")+4:command.find("=")]] = False
            #Access boolean dictionary and then translate values to True or False
        elif brain.containsChar(command):
            print("char")
            command = brain.removeSpaces(command)
            var = ""
            var = command[4:command.find("=")]
            self.funcs[function][1][var] = command[command.find("=")+1:]
            print(var+"="+self.funcs[function][1][var])
        elif brain.isContract(command):
            pass
        elif brain.updateValue(command):
            command = brain.removeSpaces(command)
            print("sup function",command)
            print(isinstance(self.funcs[function][1][command[command.find("=")-2]],int))
            if isinstance(self.funcs[function][1][command[command.find("=")-2]],int):  #Need to change, because strings can added to with +=
                if command[command.find("=")-1]=="*":
                    #print("key",command[:command.find("=")-1])
                    self.funcs[function][1][command[:command.find("=")-1]]*=int(command[command.find("=")+1:])
                elif command[command.find("=")-1]=="/":
                    self.funcs[function][1][command[:command.find("=")-1]]/=int(command[command.find("=")+1:])
                elif command[command.find("=")-1]=="+":
                    self.funcs[function][1][command[:command.find("=")-1]]+=int(command[command.find("=")+1:])
                elif command[command.find("=")-1]=="-":
                    self.funcs[function][1][command[:command.find("=")-1]]-=int(command[command.find("=")+1:])
            elif isinstance(self.funcs[function][1][command[command.find("=")-2]],str):
                if command[command.find("=")-1]=="+":
                    self.funcs[function][1][command[command.find("=")-2]]+=command[command.find("=")+1:]
                else:
                    print("Error! Invalid syntax")
            else:
                print("Error! Invalid syntax")
        elif brain.printStatement(command) and not "for" in command and not "while" in command and not "if" in command:
            print("Helllllooooooooooooooo Bigggg boyyyyyyyy")
            print(command[command.find("(")+1:command.find(")")] in self.funcs[self.functionName][1])
            if "''" in command:
                print(command[command.find("(")+1:command.find(")")])
            elif command[command.find("(")+1:command.find(")")] in self.funcs[self.functionName][1]:
                print("Ayyyyyyyy Lmaooo")
                print(self.funcs[function][1][command[command.find("(")+1:command.find(")")]])
            else:
                print(self.functionSetValue(command,function))
        elif brain.isComparison(command):
            brain.comparison(command)
        elif brain.containsArray(command):
            command = brain.removeSpaces(command)
            try:
                if command[:3] == "int":
                    self.funcs[function][1][command[command.find("]")+1:command.find("=")]] = [0 for row in range(int(command[command.find(",")+1:command.find(")")]))]
                elif command[:6] == "string":
                    self.funcs[function][1][command[command.find("]")+1:command.find("=")]] = ["Hello" for row in range(int(command[command.find(",")+1:command.find(")")]))]
                elif command[:4] == "char":
                    self.funcs[function][1][command[command.find("]")+1:command.find("=")]] = ["C" for row in range(int(command[command.find(",")+1:command.find(")")]))]
                elif command[:4] == "bool":
                    self.funcs[function][1][command[command.find("]")+1:command.find("=")]] = [True for row in range(int(command[command.find(",")+1:command.find(")")]))]
            except:
                print("Error! Invalid syntax")

        elif self.setFuncValue(command):  #Crossing variable scopes from function to overall program (only local in c0)
            command = brain.removeSpaces(command)
            if command[:3] == "int":
                self.vars[command[3:command.find("=")]] = self.funcs[function][1]["return"]
            elif command[:6] == "string":
                self.vars[command[6:command.find("=")]] = self.funcs[function][1]["return"]
            elif command[:4] == "char" or command[:4] == "bool":
                self.vars[command[4:command.find("=")]] = self.funcs[function][1]["return"]


    def storeParameters(self,command,function):
        for param in command[command.find("(")+1:command.find(")")].split(","):
            param = brain.removeSpaces(param)
            print("parameter",param)
            if param[:3] == "int":
                self.funcs[function][1][param[3:]] = 0
            elif param[:6] == "string":
                self.funcs[function][1][param[6:]] = ""
            elif param[:4] == "char":
                self.funcs[function][1][param[4:]] = ''
            elif param[:4] == "bool":
                self.funcs[function][1][param[4:]] = False

    def functionStoreValue(self,command,function):
        if "for" in command or "while" in command or "if" in command:
            self.funcs[function][0].append(command)
        else:
            self.funcs[function][0].append(command[:command.find(";")])



    def loops(self,command):
        command = brain.removeSpaces(command)
        if "for" in command:
            iterator = command[command.find("for")+4:command.find("=")]
            print("i",iterator)
            low = int(command[command.find("=")+1:command.find(";")])
            second = command[command.find(";")+1:]
            for char in second:
                if char in ["<=",">=","<",">"]:
                    p = second.find(char)
            try:
                high = int(second[p+1:second.find(";")])
                for iterator in range(low,high):
                    for line in command[command.find("{")+1:command.find("}")].split(";"):
                        print("line",line)
                        if not self.functionCalled:
                            self.vars["i"] = iterator
                            #print(self.vars)
                            if "for" in line or "while" in line or "if" in line:
                                self.loops(line)
                            else:
                                self.setValue(line)
                        else:
                            self.funcs[self.functionName][1]["i"] = iterator
                            if "for" in line or "while" in line or "if" in line:
                                self.loops(line)
                            else:
                                print("skjdnflasjgbalsiughlaiufbi")
                                self.functionSetValue(line,self.functionName)
                    #print(command[command.find("for")+4:command.find("=")],iterator)
                    #self.setValue(command[command.find("{")+1:command.find("}")])
                    #print(second[second.find("(")+3:second.find("}")-3])
            except:
                print("Error! Invalid syntax")
        elif "while" in command:
            for i in range(len(command)-1):
                if command[i] in ["==","!=","<=",">=","<",">"]:
                    p = i
                    chara = command[i]
                elif command[i:i+2] in ["==","!=","<=",">=","<",">"]:
                    p = i
                    chara = command[i:i+2]
            print("character",chara)
            try:
                iterator = command[command.find("while")+6:p]
                try:
                    if len(chara)==1:
                        ender = int(command[p+1:command.find(")")])
                    else:
                        ender = int(command[p+2:command.find(")")])
                except:
                    if len(chara)==1:
                        ender = command[p+1:command.find(")")]
                        if ender in self.vars:
                            ender = self.vars[ender]
                        elif ender in self.funcs[self.functionName][1]:
                            ender = self.funcs[self.functionName][1][ender]
                    else:
                        ender = command[p+2:command.find(")")]
                print("ekjbceljvbl3ejrv",isinstance(ender,int))
                print("char",chara)
                if chara == "==":
                    if not isinstance(self.vars[iterator],bool):
                        if not self.functionCalled:
                            while self.vars[iterator] == ender:
                                #self.setValue(command[command.find("{")+1:command.find("}")])
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                        else:
                            while self.funcs[self.functionName][1][iterator] == ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if":
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)
                    else:
                        if not self.functionCalled:
                            while self.vars[iterator] == brain.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                        else:
                             while self.funcs[self.functionName][1][iterator] == brain.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)
                elif chara == "!=":
                    if not isinstance(self.vars[iterator],bool):
                        if not self.functionCalled:
                            while self.vars[iterator] != ender:
                                #self.setValue(command[command.find("{")+1:command.find("}")])
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                        else:
                            while self.funcs[self.functionName][1][iterator] != ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else: 
                                        self.functionSetValue(line,self.functionName)
                    else:
                        if not self.functionCalled:
                            while self.vars[iterator] != self.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                        else:
                            while self.funcs[self.functionName][1][iterator] != ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)
                elif chara == "<=":
                    if not self.functionCalled:
                        while self.vars[iterator] <= ender:
                            #self.setValue(command[command.find("{")+1:command.find("}")])
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        while self.funcs[self.functionName][1][iterator] <= ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSetValue(line,self.functionName)
                elif chara == ">=":
                    if not self.functionCalled:
                        while self.vars[iterator] >= ender:
                            #self.setValue(command[command.find("{")+1:command.find("}")])
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        while self.funcs[self.functionName][1][iterator] >= ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSetValue(line,self.functionName)
                elif chara == "<":
                    print("in there")
                    print("function?",self.functionCalled)
                    if not self.functionCalled:
                        while self.vars[iterator] < ender:
                            #self.setValue(command[command.find("{")+1:command.find("}")])
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                print("line no function",line)
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        print("Command",command)
                        while self.funcs[self.functionName][1][iterator] < ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                print("line",line)
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    print("Macbook!!!")
                                    self.functionSetValue(line,self.functionName)
                                print("For loop is complete")
                elif chara == ">":
                    if not self.functionCalled:
                        while self.vars[iterator] > ender:
                            #self.setValue(command[command.find("{")+1:command.find("}")])
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        while self.funcs[self.functionName][1][iterator] > ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSetValue(line,self.functionName)
            except:
                print("helloerro")
                print("Error! Invalid syntax")
        elif "if" in command:
            for i in range(len(command)-1):
                if command[i] in ["==","!=","<=",">=","<",">"]:
                    p = i
                    chara = command[i]
                elif command[i:i+2] in ["==","!=","<=",">=","<",">"]:
                    p = i
                    chara = command[i:i+2]
            print("if character",chara)
            try:
                iterator = command[command.find("if")+3:p]
                try:
                    if len(chara)==1:
                        ender = int(command[p+1:command.find(")")])
                    else:
                        ender = int(command[p+2:command.find(")")])
                except:
                    if len(chara)==1:
                        ender = command[p+1:command.find(")")]
                        if ender in self.vars:
                            ender = self.vars[ender]
                        elif ender in self.funcs[self.functionName][1]:
                            print("Hello Moto")
                            ender = self.funcs[self.functionName][1][ender]
                    else:
                        ender = command[p+2:command.find(")")]
                        if ender in self.vars:
                            ender = self.vars[ender]
                        elif ender in self.funcs[self.functionName][1]:
                            print("Hello Moto")
                            ender = self.funcs[self.functionName][1][ender]
                    print("ender",ender)
                if chara == "==":
                    if not self.functionCalled:
                        if not isinstance(self.vars[iterator],bool):
                            if self.vars[iterator] == ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                        else:
                            if self.vars[iterator] == self.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                    else:
                        if not isinstance(self.funcs[self.functionName][1][iterator],bool):
                            if self.funcs[self.functionName][1][iterator] == ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    print("hhhhh",line)
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)
                        else:
                            if self.funcs[self.functionName][1][iterator] == self.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)

                elif chara == "!=":
                    if not self.functionCalled:
                        if not isinstance(self.vars[iterator],bool):
                            if self.vars[iterator] != ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                        else:
                            if self.vars[iterator] != self.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if":
                                        self.loops(line)
                                    else:
                                        self.setValue(line)
                    else:
                        if not isinstance(self.funcs[self.functionName][1][iterator],bool):
                            if self.funcs[self.functionName][1][iterator] != ender:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)
                        else:
                            if self.funcs[self.functionName][1][iterator] != self.Boolean[ender]:
                                for line in command[command.find("{")+1:command.find("}")].split(";"):
                                    if "for" in line or "while" in line or "if" in line:
                                        self.loops(line)
                                    else:
                                        self.functionSetValue(line,self.functionName)
                elif chara == "<=":
                    if not self.functionCalled:
                        if self.vars[iterator] <= ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        if self.funcs[self.functionName][1][iterator] <= ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSetValue(line,self.functionName)
                elif chara == ">=":
                    if not self.functionCalled:
                        if self.vars[iterator] >= ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        if self.funcs[self.functionName][1][iterator] >= ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSet(line,self.functionName)
                elif chara == "<":
                    if self.functionCalled:
                        if self.vars[iterator] < ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        if self.funcs[self.functionName][1][iterator] < ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSetValue(line,self.functionName)
                elif chara == ">":
                    if self.functionCalled:
                        if self.vars[iterator] > ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.setValue(line)
                    else:
                        if self.funcs[self.functionName][1][iterator] > ender:
                            for line in command[command.find("{")+1:command.find("}")].split(";"):
                                if "for" in line or "while" in line or "if" in line:
                                    self.loops(line)
                                else:
                                    self.functionSetValue(line,self.functionName)
            except:
                print("Error! Invalid syntax")


    def getValue(self,var):
        print(self.vars[var])

    def functionGetValue(self,var,function):
        print(self.funcs[function][1][var])

    def printVars(self):
        print(self.vars)

    def functionPrintVars(self,function):
        print(self.funcs[function][1])
        #print(self.funcs)


#compiler = brain()
#compiler.loops("for (i = 0; i< 10; i++){print(""hello"")}")


"""
#Testing the compiler
boyy = brain()
print(brain.containsInt("int x=1"))
boyy.setValue("int x=1")
boyy.getValue("x")
print(brain.isComment("/*Here is my compiler*/"))
print(brain.containsString("string s=words"))
print(brain.containsChar("char c=h"))
print(brain.operator(" 6 * 3"))
s = "string s=hello;int x=1"
for command in s.split(";"):
    print("string?",brain.containsString(command))
    print("int?",brain.containsInt(command))
print(brain.containsBool("bool b=true"))
print(brain.comparisons("False  ^   False "))  #Work on comparisons
print(brain.isContract("//@requires x=1"))
boyy.setValue("string s = words")
boyy.getValue("s")
boyy.setValue("bool b = true")
boyy.getValue("b")
print(boyy.vars)
boyy.vars["x"]*=4
print(boyy.vars)
boyy.vars["b"]="false"
print(boyy.vars)
boyy.setValue("char c = a")
boyy.getValue("c")
print(boyy.vars)
boyy.setValue("int y = 121")
boyy.getValue("y")
print(boyy.vars)
boyy.vars["y"]//=11
print(boyy.vars)"""
print(brain.containsFunction(
"""int log(int x)
//@requires x >= 1;
//@ensures \result >= 0;
{ int r = 0;
  while (x > 1) {
    x = x / 2;
    r = r + 1;
  }
  return r;
}

    """))





