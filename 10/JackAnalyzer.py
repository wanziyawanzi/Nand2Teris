#编译器1：语法分析
keyword_list=['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
            'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
symbol_list=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']

class JackTokenizer:    #分词器
    def __init__(self,jack_file):
        with open (jack_file,'r') as f:
            self.content=f.read()
        self.current_token=None
        self.tokens=[]
        self.pos=0
    
    def hasMoreTokens(self):    #是否还有下一个char
        return self.pos<len(self.content)
    def peek(self):         #获取当前char,索引不变
        if self.hasMoreTokens():
            char=self.content[self.pos]
            return char
        return None
    def peek_next(self):    #获取后一位char,索引不变
        if (self.pos+1)<len(self.content):
            next_pos=self.pos+1
            char=self.content[next_pos]
            return char
        return None
    def advance(self):      #获取当前char,索引后移一位
        if self.hasMoreTokens():
            char=self.content[self.pos]
            self.pos+=1
            return char
        return None
    def skip_comment(self):     #跳过注释符/
        self.advance()
        if self.peek()=='*':
            while self.hasMoreTokens() and not(self.peek()=='*'and self.peek_next()=='/'):
                self.advance()
            self.advance()
            self.advance()
            return
        elif self.peek()=='/':
            while self.hasMoreTokens() and self.peek()!='\n':
                self.advance()   

    def read_string(self):
        self.advance()
        string_val=''
        while self.hasMoreTokens() and self.peek() != '"':
            string_val+=self.advance()
        if self.hasMoreTokens():   
            self.advance()
        return ('stringConstant',string_val)
    def read_int(self):
        int_val=''
        while self.hasMoreTokens() and self.peek().isdigit():
            int_val+=self.advance()
        return ('integerConstant',int_val)
    def read_keyword_or_identifier(self):
        word=''
        while self.hasMoreTokens() and (self.peek().isalpha() or self.peek()=='_' or self.peek().isdigit()):
            word+=self.advance()
        if word in keyword_list:
            return ('keyword',word)
        else:
            return ('identifier',word)

    def tokenizen(self):
        while self.hasMoreTokens():
            char=self.peek()
            if char.isspace():
                self.advance()
                continue
            if char=='/' and self.peek_next()in ('/','*'):
                self.skip_comment()
                continue
            if char in symbol_list:     #符号
                self.tokens.append(('symbol',self.advance()))   #元组
                continue
            if char=='"':       #字符串常量
                self.tokens.append(self.read_string())
                continue
            if char.isdigit():  #整数常量
                self.tokens.append(self.read_int())
                continue
            if char.isalpha() or char=='_':
                self.tokens.append(self.read_keyword_or_identifier())
                continue
            raise ValueError(f'非法字符：{char}')

class CompilationEngine:    #编译引擎
    def __init__(self,tokens):
        self.tokens=tokens
        self.index=0
        self.output=[]
        self.current_token=self.tokens[self.index]
    def eat(self):
        pass
    def compileClass(self):
        self.output.append('<class>')
        
        self.output.append('</class>')

import os;import glob
input_path=r'C:\Users\23981\Desktop\nand2tetris\projects\10\Square'
output_path=r'C:\Users\23981\Desktop\nand2tetris\projects\10\Testout'
jack_files=sorted(glob.glob(f'{input_path}\\*.jack'))   #返回路径下所有jack文件,类型为list,sorted为排序函数

for jack_file in jack_files:    #遍历jack文件
    tokenizer=JackTokenizer(jack_file)
    tokenizer.tokenizen()      #纯粹工具，无返回值，不保存结果，访问属性在tokens[]里
    vm_file=os.path.join(output_path,(os.path.basename(jack_file).replace('.jack','.xml') ))   #设置路径和文件名
    jackcompiler=CompilationEngine(vm_file)
    jackcompiler.compileClass()
    with open(vm_file,'w') as f:
        f.write('<tokens>\n')
        for token in tokenizer.tokens:
            token_type,token_value=token
            token_value_rep=token_value.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
            f.write (f'<{token_type}> {token_value_rep} </{token_type}>\n')
        f.write('</tokens>\n')

