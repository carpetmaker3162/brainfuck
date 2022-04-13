from brainfuck import BrainfuckInterpreter

if __name__ == "__main__":
    prog = """++++++++[>++++[>++>+++>+++>+<<<<-]
    >+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.
    +++.------.--------.>>+.>++."""
    
    not_verbose = BrainfuckInterpreter(prog)
    verbose = BrainfuckInterpreter(prog, verbose=True)