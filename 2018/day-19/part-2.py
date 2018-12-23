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
    registers = [1, 0, 0, 0, 0, 0]
    # registers = [0, 10551292, 4, 10551293, 10551293, 1]
    # registers = [1, 10551292, 13, 10551293, 0, 10551293]
    count = 0
    while registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        name = instruction[0]
        operation = name_to_operation[name]
        registers = operation(registers, instruction)
        registers[instruction_pointer] += 1
        count += 1
        print(registers)
        if count == 500:
            break
    return registers


if __name__ == '__main__':
    instruction_pointer, instructions = parse_input('input.txt')
    registers = execute_instructions(instruction_pointer, instructions)
    print(registers[0])

    # instruction_pointer, instructions = parse_input('test-input.txt')
    # registers = execute_instructions(instruction_pointer, instructions)
    # print(registers[0])

# Solution:
# 1+2+4+61+83+122+166+244+332+521+1042+2084+5063+
# 10126+20252+31781+43243+63562+86486+127124+172972+
# 2637823+5275646+10551292 = 19030032

# This was done by discovering the pattern to the inputs causing a pattern in the
# registers. The pattern was that registers[3] would increment until
# registers[3] * registers[5] == 10551292 (registers[1]). Once that happened,
# registers[5] would be added to registers[0] and then registers[5] would be
# incremented by 1 and registers[3] set back to 1. This continued until
# registers[5] > 10551292 (registers[1]) which would finally break the loop.

# The final value of registers[0] was thus the divisors of 10551292 since the
# only time registers[0] would be added to was when
# registers[3] * registers[5] = 10551292 and registers[5] was added.
