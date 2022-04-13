# Added verbose mode for debugging

# okay so I found out that my original understanding of brainfuck loops was incorrect...
# originally I thought that every time a loop is initialized, the counter is permanently
# set to whatever cell the ptr is at when the program arrives at the loop. So I wasted a 
# lot of trouble storing the counter permanently inside a dictionary. But when I was
# experimenting with brainfuck programs I noticed that a lot of programs got stuck in
# infinite loops. At first I ignored it and just blamed it on whoever wrote the brainfuck
# programs but it turned out I misunderstood how brainfuck loops work. Now the
# implementation is much cleaner and actually works properly

class BrainfuckInterpreter:
    def __init__(self, bfcode, verbose=False):
        self.ptr = 0
        self.array = [0 for _ in range(30000)]
        self.validchars = (">", "<", "+", "-", ".", ",", "[", "]")
        self.bfcode = bfcode
        self.output = ""
        self.reason = None
        self.runningloops = []
        self.loops = self.all_loops(self.bfcode)
        self.verbose = verbose
        self.interpret()

    def interpret(self):
        position = 0
        while position < len(self.bfcode):
            instruction = self.bfcode[position]

            if instruction == ".":
                if self.verbose and self.array[self.ptr] == 10: print(f"Printing character NEWLINE (pos {position}/{len(self.bfcode)-1})")
                elif self.verbose and self.array[self.ptr] != 10: print(f"Printing character '{chr(self.array[self.ptr])}' (pos {position}/{len(self.bfcode)-1})")
                self.output += chr(self.array[self.ptr])

            if instruction == ",":
                if self.verbose: print(f"Waiting for user input... (pos {position}/{len(self.bfcode)-1})")
                new_input = input()
                if len(new_input) != 1:
                    print("invalid input")
                    break
                self.array[self.ptr] = ord(new_input)
            
            if instruction == ">":
                if self.verbose: print(f"Moving pointer right... (pos {position}/{len(self.bfcode)-1})")
                if self.ptr == 29999:
                    position += 1
                    continue
                self.ptr += 1
            
            if instruction == "<":
                if self.verbose: print(f"Moving pointer left... (pos {position}/{len(self.bfcode)-1})")
                if self.ptr == 0:
                    position += 1
                    continue
                self.ptr -= 1
            
            if instruction == "+":
                if self.verbose: print(f"Incrementing cell {self.ptr}... (pos {position}/{len(self.bfcode)-1})")
                if self.array[self.ptr] == 255:
                    self.array[self.ptr] = 0
                    continue
                self.array[self.ptr] += 1
            
            if instruction == "-":
                if self.verbose: print(f"Decrementing cell {self.ptr}... (pos {position}/{len(self.bfcode)-1})")
                if self.array[self.ptr] == 0:
                    self.array[self.ptr] = 255
                    continue
                self.array[self.ptr] -= 1

            if instruction == "[":
                if self.verbose: print(f"Entering loop... (pos {position}/{len(self.bfcode)-1})")
                if self.array[self.ptr] == 0:
                    if self.verbose: print(f"Exiting loop... (pos {position}/{len(self.bfcode)-1})")
                    position = self.loops[position] + 1
                    continue
            
            if instruction == "]":
                if self.array[self.ptr] == 0:
                    if self.verbose: print(f"Exiting loop... (pos {position}/{len(self.bfcode)-1})")
                    position += 1
                    continue
                if self.verbose: print(f"Jumping back to cell {self.loops[position]}... (pos {position}/{len(self.bfcode)-1})")
                position = self.loops[position]

            position += 1
        if self.output:
            if self.verbose:
                print("EOF\n\n\n----Output----")
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