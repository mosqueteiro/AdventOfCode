"""
--- Day 17: Chronospatial Computer ---

--------------------- Part I ---------------------
The program output: (1,6,3,6,5,6,5,1,7)
Took 9.753e-05 s to run.

"""


from dataclasses import dataclass
from io import StringIO
from time import perf_counter
from typing import TextIO

@dataclass
class ChronospatialComputer:
    A: int
    B: int
    C: int
    prog: list[int]

    def __post_init__(self):
        self.opcounter = 0
        self.prog_pntr: int = 0
        self.out_stream: StringIO = StringIO()
        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def clear(self) -> None:
        self.__post_init__()

    def run_prog(self) -> None:
        while self.prog_pntr < (len(self.prog) - 1):
            self.opcounter += 1
            check_pntr = self.prog_pntr
            opcode = self.prog[self.prog_pntr]
            arg = self.prog[self.prog_pntr+1]
            self.opcodes[opcode](arg)
            if self.prog_pntr == check_pntr:
                self.prog_pntr += 2

    def eval_operand(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            raise RuntimeError("Invalid Operand, Invalid Program.")

    def adv(self, operand: int) -> None:
        self.A = self.A // (2 ** self.eval_operand(operand))

    def inv_adv(self, operand: int) -> list[int]:
        n_0 = self.A * (2 ** self.eval_operand(operand))
        n_f = (self.A + 1) * (2 ** self.eval_operand(operand))
        return list(range(n_0, n_f))

    def bxl(self, operand: int) -> None:
        self.B = self.B ^ operand

    def bst(self, operand: int ) -> None:
        self.B = self.eval_operand(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.A == 0:
            return
        self.prog_pntr = operand

    def bxc(self, operand: int) -> None:
        _ = operand
        self.B = self.B ^ self.C

    def out(self, operand: int) -> None:
        result = str(self.eval_operand(operand) % 8)
        if self.out_stream.tell() > 0:
            self.out_stream.write(",")
        self.out_stream.write(result)

    def bdv(self, operand: int) -> None:
        self.B = self.A // (2 ** self.eval_operand(operand))

    def cdv(self, operand: int) -> None:
        self.C = self.A // (2 ** self.eval_operand(operand))


def parse_debugger(file: TextIO) -> ChronospatialComputer:
    computer_args = {}
    while line := file.readline():
        match line.split():
            case ["Register", register, value]:
                computer_args[register[0]] = int(value)
            case ["Program:", program]:
                prog = list(int(num) for num in program.split(","))
                computer_args["prog"] = prog
    return ChronospatialComputer(**computer_args)

def prog_analyzer(prog: list[int]) -> int:
    # ops = []
    # args = []
    # it_prog = iter(prog)
    # for i in it_prog:
    #     ops.append(i)
    #     args.append(next(it_prog))
    prog_pntr = 0
    prog_last_arg = len(prog) - 1
    while prog_pntr < prog_last_arg:
        match prog[prog_pntr]:
            case _:
                return 0



if __name__ == "__main__":
    from adventofcode import arg_parser_init, print_part_divider


    parser = arg_parser_init()
    args = parser.parse_args()

    if args.test:
        file = open("example.txt", "r")
    elif args.f:
        file = args.f
    else:
        raise Exception("Either a file or test must be passed.")

    computer = parse_debugger(file)
    file.close()

    print_part_divider("Part I")
    start = perf_counter()
    computer.run_prog()
    elapsed = perf_counter() - start
    computer.out_stream.seek(0)
    out = computer.out_stream.read()
    print(f"The program output: ({out})")
    print(f"Took {elapsed:.3e} s to run.")

    if args.test:
        c1 = ChronospatialComputer(**{
            "A": 0,
            "B": 0,
            "C": 9,
            "prog": [2,6],
        })
        c1.run_prog()
        assert c1.B == 1
        c2 = ChronospatialComputer(**{
            "A": 10,
            "B": 0,
            "C": 0,
            "prog": [5,0,5,1,5,4]
        })
        c2.run_prog()
        assert c2.out_stream.getvalue() == "0,1,2", f"Wrong output: ({c2.out_stream.getvalue()})"
        c3 = ChronospatialComputer(**{
            "A": 2024,
            "B": 0,
            "C": 0,
            "prog": [0,1,5,4,3,0]
        })
        c3.run_prog()
        assert c3.out_stream.getvalue() == "4,2,5,6,7,7,7,7,3,1,0", f"Wrong output: ({c3.out_stream.getvalue()})"
        c4 = ChronospatialComputer(**{
            "A": 0,
            "B": 29,
            "C": 0,
            "prog": [1,7],
        })
        c4.run_prog()
        assert c4.B == 26
        c5 = ChronospatialComputer(**{
            "A": 0,
            "B": 2024,
            "C": 43690,
            "prog": [4,0]
        })
        c5.run_prog()
        assert c5.B == 44354

        ans = "4,6,3,5,6,3,5,2,1,0"
        assert out == ans, f"The output did not match expected: ({ans})"

    print_part_divider("Part II")
    if args.test:
        computer = ChronospatialComputer(**{
            "A": 2024,
            "B": 0,
            "C": 0,
            "prog": [0,3,5,4,3,0]
        })
    start = perf_counter()
    prog = computer.prog
    reg_a_init = prog_analyzer(prog)
    computer.clear()
    computer.A = reg_a_init
    computer.run_prog()
    elapsed = perf_counter() - start
    assert computer.out_stream.getvalue() == prog, "Programs do not match"
    print(f"The lowest initial value for Register A: {reg_a_init}")
    print(f"Took {elapsed:.3e} s to run.")

    if args.test:
        ans = 117440
        assert reg_a_init == ans, f"The Register A initializer value didn't match expected ({ans})"

