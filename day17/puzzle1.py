import math

def adv_exec(cpu, operand):
    cpu.registers[0] = math.trunc(cpu.registers[0] / (2 ** operand))

def bxl_exec(cpu, operand):
    cpu.registers[1] = cpu.registers[1] ^ operand

def bst_exec(cpu, operand):
    cpu.registers[1] = operand % 8

def jnz_exec(cpu, operand):
    if cpu.registers[0] != 0:
        cpu.pc = operand

def bxc_exec(cpu, operand):
    cpu.registers[1] = cpu.registers[1] ^ cpu.registers[2]

def out_exec(cpu, operand):
    cpu.output.append(operand % 8)

def bdv_exec(cpu, operand):
    cpu.registers[1] = math.trunc(cpu.registers[0] / (2 ** operand))

def cdv_exec(cpu, operand):
    cpu.registers[2] = math.trunc(cpu.registers[0] / (2 ** operand))

CPU_REGISTERS = [ "A", "B", "C" ]
READ_LITERAL = 0
READ_COMBO_OP = 1
INSTRUCTION_SET = {
    0: {
        "name": "adv",
        "description": "Divides the A register by 2 raised to the power of the combo operand represented value, truncates the result, and stores it in the A register",
        "read_type": READ_COMBO_OP,
        "exec": adv_exec
    },
    1: {
        "name": "bxl",
        "description": "Bitwise XORs the B register with literal operand, result is stored in B",
        "read_type": READ_LITERAL,
        "exec": bxl_exec
    },
    2: {
        "name": "bst",
        "description": "Value represented by the combo operand mod 8 (keeping the last 3 bits), result is stored in B",
        "read_type": READ_COMBO_OP,
        "exec": bst_exec
    },
    3: {
        "name": "jnz",
        "description": "Does nothing if A is 0, otherwise jumps to the instruction at the literal operand address",
        "read_type": READ_LITERAL,
        "exec": jnz_exec
    },
    4: {
        "name": "bxc",
        "description": "Bitwise XORs registers B and C, result is stored in B",
        "read_type": READ_LITERAL, # Ignored
        "exec": bxc_exec
    },
    5: {
        "name": "out",
        "description": "Value represented by the combo operand mod 8 (keeping the last 3 bits), result is stored output to the screen followed by a comma",
        "read_type": READ_COMBO_OP,
        "exec": out_exec
    },
    6: {
        "name": "bdv",
        "description": "Divides the A register by 2 raised to the power of the combo operand represented value, truncates the result, and stores it in B",
        "read_type": READ_COMBO_OP,
        "exec": bdv_exec
    },
    7: {
        "name": "cdv",
        "description": "Divides the A register by 2 raised to the power of the combo operand represented value, truncates the result, and stores it in C",
        "read_type": READ_COMBO_OP,
        "exec": cdv_exec
    }
}

class CPU:
    def __init__(self, registers: list, program: list):
        self.registers = registers
        self.program = program
        self.pc = 0
        self.output = []

        assert len(self.registers) == len(CPU_REGISTERS)
        assert len(self.program) % 2 == 0

    def read_op(self) -> int:
        value = self.program[self.pc]
        self.pc += 1
        return value

    def read_combo_op(self) -> int:
        value = self.read_op()
        if value >= 0 and value <= 3:
            return value
        elif value >= 4 and value <= 6:
            return self.registers[value - 4]
        else:
            raise Exception(f"Invalid combo operand value: {value}")

    def has_reached_end(self) -> bool:
        return self.pc >= len(self.program)

    def dump(self):
        print(f"Registers: {self.registers}")
        print(f"Program: {self.program}")
        print(f"PC: {self.pc}")
        print(f"Output: {self.output}")

    def run(self):
        # Run the program
        while not self.has_reached_end():
            opcode = self.read_op()
            if opcode not in INSTRUCTION_SET:
                raise Exception(f"Invalid opcode: {opcode}")
            instruction = INSTRUCTION_SET[opcode]

            operand = None
            if instruction["read_type"] == READ_LITERAL:
                operand = self.read_op()
            elif instruction["read_type"] == READ_COMBO_OP:
                operand = self.read_combo_op()
            else:
                raise Exception(f"Invalid read type: {instruction['read_type']}")

            instruction["exec"](self, operand)

        # Print the output
        print(",".join(map(str, self.output)))

def read_input(file: str) -> CPU:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    registers = [0] * len(CPU_REGISTERS)
    program = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        if cleaned_line.startswith("Register "):
            parts = cleaned_line.split(":")
            reg_name = parts[0].split(" ")[1].strip()
            reg_val = int(parts[1].strip())

            if reg_name in CPU_REGISTERS:
                registers[CPU_REGISTERS.index(reg_name)] = reg_val
            else:
                raise Exception(f"Invalid register name: {reg_name}")
        elif cleaned_line.startswith("Program: "):
            parts = cleaned_line.split(":")[1].strip().split(",")
            program = list(map(int, parts))
        else:
            raise Exception(f"Invalid line: {cleaned_line}")

    return CPU(registers, program)

cpu = read_input("input.txt")
cpu.run()
