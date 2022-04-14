from brainfuck import BrainfuckInterpreter

prog = "-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------."
BrainfuckInterpreter(prog, verbose=False)
BrainfuckInterpreter(prog, verbose=True)