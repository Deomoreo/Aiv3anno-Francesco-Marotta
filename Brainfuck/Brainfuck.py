from asyncore import loop
from logging import exception

class HeadOverflow(Exception):
    pass

class BracketMismatch(Exception):
    pass

class BrainfuckMachine:

    MAPPINGS = {
    '+': 'add',
    '-': 'subtract',
    '>': 'increment_pointer',
    '<': 'decrement_pointer',
    '[': 'skip_open',
    ']': 'skip_close'
}
    HeadOverflow = HeadOverflow
    BracketMismatch = BracketMismatch
    def __init__(self,tapeLenght) -> None:
                self.tape = bytearray(tapeLenght)
                self.head = 0
                self.instruction_pointer = 0
                self.code = ''
                self.pairs = {}
                self.stack = []
                self.parens = self.find_pairs(self.code)
                


    def find_pairs(self, program):
        loopCounter = 0
        for i, c in enumerate(program):
            if c == '[':
                j = i + 1
                if program[j]== '[':
                    print('hello')
                    raise self.BracketMismatch("BracketError")
                while j < len(program):
                    if program[j] == '[':
                        loopCounter += 1
                    if program[j] == ']':
                        if loopCounter > 0:
                            loopCounter -= 1
                        else:
                             self.pairs[i] = j
                             self.pairs[j] = i
                             break   
                    j += 1
                
    def run(self):
        self.find_pairs(self.code)
        while self.instruction_pointer < len(self.code):
            func = self.MAPPINGS.get(self.code[self.instruction_pointer])
            
            if func == 'add':
                self.add()
            if func == 'subtract':
                self.subtract()
            if func == 'increment_pointer':
                self.increment_pointer()
            if func == 'decrement_pointer':
                self.decrement_pointer()
            if func == 'skip_open':
                self.skip_open()
            if func == 'skip_close':
                self.skip_close()         
            self.instruction_pointer += 1
            

    def add(self):
        if self.tape[self.head] +1 > 255:
            self.tape[self.head] = 0
        else: self.tape[self.head] += 1    
    def subtract(self):
        if self.tape[self.head] -1 < 0:
            self.tape[self.head] = 255
        else: self.tape[self.head] -= 1
    def increment_pointer(self):
        if self.head +1 < len(self.tape):
            self.head += 1
        else: 
            raise self.HeadOverflow("HeadOverflow")     
    def decrement_pointer(self):
        if self.head -1 >= 0:
            self.head -= 1
        else: 
            raise self.HeadOverflow("HeadOverflow")       

    def skip_open(self):
        currentByte = self.tape[self.head]
        if currentByte > 0:
            self.stack.append(self.instruction_pointer - 1) 
        else: self.instruction_pointer = self.pairs[self.instruction_pointer]    
    def skip_close(self):
        currentByte = self.tape[self.head]
        if currentByte == 0:
            self.instruction_pointer = self.stack.pop()  
        else:   
            self.instruction_pointer = self.pairs[self.instruction_pointer]

    
    


        