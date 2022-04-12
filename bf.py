import sys
import time

class BrainfuckInterpreter:
    def __init__(self, bfcode):
        self.ptr = 0
        self.array = [0 for _ in range(30000)]
        self.validchars = (">", "<", "+", "-", ".", ",", "[", "]")
        self.bfcode = bfcode
        self.output = ""
        self.reason = None
        self.runningloops = []
        self.loops = self.all_loops(self.bfcode)
        self.interpret()

    def interpret(self):
        position = 0
        while position < len(self.bfcode):
            instruction = self.bfcode[position]

            if instruction == ".":
                self.output += chr(self.array[self.ptr])

            if instruction == ",":
                new_input = input()
                if len(new_input) != 1:
                    print("invalid input")
                    break
                self.array[self.ptr] = ord(new_input)
            
            if instruction == ">":
                if self.ptr == 29999:
                    position += 1
                    continue
                self.ptr += 1
            
            if instruction == "<":
                if self.ptr == 0:
                    position += 1
                    continue
                self.ptr -= 1
            
            if instruction == "+":
                if self.array[self.ptr] == 255:
                    self.array[self.ptr] = 0
                    continue
                self.array[self.ptr] += 1
            
            if instruction == "-":
                if self.array[self.ptr] == 0:
                    self.array[self.ptr] = 255
                    continue
                self.array[self.ptr] -= 1

            if instruction == "[":
                if type(self.loops[position]) != tuple:
                    self.loops[position] = (self.loops[position], self.ptr)
                if self.array[self.loops[position][1]] == 0:
                    position = self.loops[position][0] + 1
                    continue
            
            if instruction == "]":
                if self.array[self.loops[self.loops[position]][1]] == 0:
                    position += 1
                    continue
                position = self.loops[position]

            position += 1
        if self.output:
            print(self.output, end='')

    def all_loops(self, code):
        _all_loops = {}
        _begin_loops = []
        for position, instruction in enumerate(code):
            if instruction == "[":
                _begin_loops.append(position)
            elif instruction == "]":
                left = _begin_loops.pop()
                right = position
                _all_loops[left] = right
                _all_loops[right] = left
        return _all_loops

if __name__ == "__main__":
    bf = BrainfuckInterpreter("+++++++++++++[>+++++<-]>.>++++++++.") # insert brainfuck code here