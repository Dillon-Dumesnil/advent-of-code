import os

from ast import literal_eval

script_dir = os.path.dirname(__file__)


def add_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] + registers[B]
    return after_op

def add_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] + B
    return after_op

def mul_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] * registers[B]
    return after_op

def mul_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] * B
    return after_op

def ban_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] & registers[B]
    return after_op

def ban_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] & B
    return after_op

def bor_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] | registers[B]
    return after_op

def bor_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A] | B
    return after_op

def set_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = registers[A]
    return after_op

def set_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = A
    return after_op

def gt_i_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = 1 if A > registers[B] else 0
    return after_op

def gt_r_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = 1 if registers[A] > B else 0
    return after_op

def gt_r_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = 1 if registers[A] > registers[B] else 0
    return after_op

def eq_i_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = 1 if A == registers[B] else 0
    return after_op

def eq_r_i(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = 1 if registers[A] == B else 0
    return after_op

def eq_r_r(registers, instruction):
    after_op = registers.copy()
    _, A, B, C = instruction
    after_op[C] = 1 if registers[A] == registers[B] else 0
    return after_op

all_operations = [
    add_r,
    add_i,
    mul_r,
    mul_i,
    ban_r,
    ban_i,
    bor_r,
    bor_i,
    set_r,
    set_i,
    gt_i_r,
    gt_r_i,
    gt_r_r,
    eq_i_r,
    eq_r_i,
    eq_r_r,
]

opcodes = {i: all_operations.copy() for i in range(16)}

def behaves_like_opcodes(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        all_lines = f.readlines()
        for i in range(0, len(all_lines), 4):
            before = literal_eval(all_lines[i].strip().split(': ')[1])
            instruction = [int(j) for j in all_lines[i + 1].strip().split()]
            after = literal_eval(all_lines[i + 2].strip().split(':  ')[1])
            opcode = instruction[0]

            for operation in all_operations:
                result = operation(before, instruction)
                if result != after:
                    if operation in opcodes[opcode]:
                        opcodes[opcode].remove(operation)

    return opcodes

def process_opcodes(opcodes):
    # This is to reduce each opcode down to a single possible operation.
    for i in range(16):
        for code in opcodes:
            if len(opcodes[code]) == 1:
                for k in opcodes:
                    if k != code and opcodes[code][0] in opcodes[k]:
                        opcodes[k].remove(opcodes[code][0])
    return opcodes

def do_instructions(input_file, opcodes):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        registers = [0, 0, 0, 0]
        for line in f:
            instruction = [int(j) for j in line.strip().split()]
            opcode = instruction[0]
            operation = opcodes[opcode][0]
            registers = operation(registers, instruction)

    return registers


if __name__ == '__main__':
    opcodes = behaves_like_opcodes('input-1.txt')
    opcodes = process_opcodes(opcodes)
    final_registers = do_instructions('input-2.txt', opcodes)
    print(final_registers)
