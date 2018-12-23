import os

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

def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        instruction_pointer = int(f.readline().strip().split()[1])
        instructions = []
        for line in f:
            instruction = line.strip().split()
            instruction[1:] = [int(i) for i in instruction[1:]]
            instructions.append(instruction)

    return instruction_pointer, instructions

name_to_operation = {
    'addr': add_r,
    'addi': add_i,
    'mulr': mul_r,
    'muli': mul_i,
    'banr': ban_r,
    'bani': ban_i,
    'borr': bor_r,
    'bori': bor_i,
    'setr': set_r,
    'seti': set_i,
    'gtir': gt_i_r,
    'gtri': gt_r_i,
    'gtrr': gt_r_r,
    'eqir': eq_i_r,
    'eqri': eq_r_i,
    'eqrr': eq_r_r,
}
def execute_instructions(instruction_pointer, instructions):
    registers = [0, 0, 0, 0, 0, 0]
    while registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        name = instruction[0]
        operation = name_to_operation[name]
        registers = operation(registers, instruction)
        registers[instruction_pointer] += 1

    return registers


if __name__ == '__main__':
    instruction_pointer, instructions = parse_input('input.txt')
    registers = execute_instructions(instruction_pointer, instructions)
    print(registers[0])

    # instruction_pointer, instructions = parse_input('test-input.txt')
    # registers = execute_instructions(instruction_pointer, instructions)
    # print(registers[0])
