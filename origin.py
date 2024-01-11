from interpreter import Token, tokenize, clean_tokens

class SharpInfo:
    
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.tokens = self.process_sharp()
        

    def process_sharp(self):
        tokens = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for token in tokenize(file.read()):
                tokens.append(token)
            tokens = clean_tokens(tokens)
        return tokens
    

    def is_period(self, index):
        if self.tokens[index].type == "PERIOD":
            return True
        else:
            return False

    def get_path(self, index):
        path = []
        index += 1
        path.append(self.tokens[index])
        while self.is_period(index + 1):
            index += 2
            path.append(self.tokens[index])
        
        return path
    
    def is_method(self, index, bol = False):
        target = self.tokens[index + 1]
        if target.type == "RPAREN":
            if self.tokens[index + 2].type == "LBRACK":
                return True
            else: 
                return False
        else: 
            bol = self.is_method((index + 1), bol)
            return bol
    
    def list_to_path(self, list):
        path = ""
        for index, i in enumerate(list):
                    path += str(i.value)
                    if list[index] != list[-1] :
                        path += "."

        return path

    @property
    def data(self):
        classes = {}
        methods = {}
        functions = {}
        using = {}
        ids = {}
        namespace = {}
        
        for index, token in enumerate(self.tokens):
            target = None
            if token.type == 'CLASS':
                target = self.tokens[index + 1]
                classes[target.value] = {
                            "line": target.line, 
                            "column" : target.column
                            }
                colon = self.tokens[index + 2]
                if colon.type == "COLON":
                    inher = self.tokens[index + 3]
                    if inher.type == "ID":
                        classes[target.value] = {
                            "line": target.line, 
                            "column" : target.column, 
                            "inheritance": inher.value
                            }

            elif token.type == 'LPAREN' and self.tokens[index - 1].type == 'ID':
                if self.is_method(index):
                    meth = self.tokens[index - 1]
                    
                    methods[meth.value] = {
                            "line": meth.line, 
                            "column" : meth.column
                            }
                else:
                    func = self.tokens[index - 1]
                    functions[func.value] = {
                            "line": func.line, 
                            "column" : func.column
                            }
            elif (token.type == 'USING') and (self.tokens[index+1].type == "ID"):
                lis = self.get_path(index)
                     
                path = self.list_to_path(lis)
                
                dependant = lis[-1]
                using[dependant.value] = {
                    "line": dependant.line,
                    'column': dependant.column,
                    "path": path
                }

            elif token.type == "ID":
                ids[token.value] = {
                            "line": token.line, 
                            "column" : token.column
                            }
            elif token.type == "NAMESPACE":
                direct = self.tokens[index + 1]
                
                namespace[direct.value] = {
                    "line": direct.line,
                    "column": direct.column
                }


    
        document = {
            "file_path": self.file_path,
            "namespace": namespace,
            "classes" : classes,
            "methods" : methods,
            "functions": functions,
            "using" : using,
            "ids" : ids

        }
        return document
    
