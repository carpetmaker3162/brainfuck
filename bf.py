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
                print(f"Printing character '{chr(self.array[self.ptr])}' (pos {position}/{len(self.bfcode)})")
                self.output += chr(self.array[self.ptr])

            if instruction == ",":
                print(f"Waiting for input... (pos {position}/{len(self.bfcode)})")
                new_input = input()
                if len(new_input) != 1:
                    self.reason = f"invalid input"
                    self.abort()
                    break
                self.array[self.ptr] = ord(new_input)
            
            if instruction == ">":
                print(f"Incrementing ptr (pos {position}/{len(self.bfcode)})")
                if self.ptr == 29999:
                    position += 1
                    time.sleep(0.0001)
                    continue
                self.ptr += 1
            
            if instruction == "<":
                print(f"Decrementing ptr (pos {position}/{len(self.bfcode)})")
                if self.ptr == 0:
                    position += 1
                    time.sleep(0.0001)
                    continue
                self.ptr -= 1
            
            if instruction == "+":
                print(f"Incrementing cell {self.ptr} (pos {position}/{len(self.bfcode)})")
                if self.array[self.ptr] == 255:
                    self.array[self.ptr] = 0
                    time.sleep(0.0001)
                    continue
                self.array[self.ptr] += 1
            
            if instruction == "-":
                print(f"Decrementing cell {self.ptr} (pos {position}/{len(self.bfcode)})")
                if self.array[self.ptr] == 0:
                    self.array[self.ptr] = 255
                    time.sleep(0.0001)
                    continue
                self.array[self.ptr] -= 1

            if instruction == "[":
                if type(self.loops[position]) != tuple:
                    print(f"Starting loop at position {position}, counter at cell {self.ptr} (pos {position}/{len(self.bfcode)})")
                    self.loops[position] = (self.loops[position], self.ptr)
                if self.array[self.loops[position][1]] == 0:
                    position = self.loops[position][0] + 1
                    print(f"Ending loop at position {position} (pos {position}/{len(self.bfcode)})")
                    time.sleep(0.0001)
                    continue
                print(f"Entering loop at position {position} (pos {position}/{len(self.bfcode)})")
            
            if instruction == "]":
                if self.array[self.loops[self.loops[position]][1]] == 0:
                    position += 1
                    print(f"Exiting loop at position {position} (pos {position}/{len(self.bfcode)})")
                    time.sleep(0.0001)
                    continue
                print(f"Jumping back to position {self.loops[position]} (pos {position}/{len(self.bfcode)})")
                position = self.loops[position]
            
            time.sleep(0.0001)
            position += 1
        if self.output:
            print("End of code reached\n\n\n----Output----")
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
        
    
    def abort(self):
        self.output = ""
        print("The interpretation was aborted.\nReason:", self.reason)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        bf = BrainfuckInterpreter(sys.argv[1])
    else:
        bf = BrainfuckInterpreter("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.") # insert brainfuck code here