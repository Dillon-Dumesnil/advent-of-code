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

def behaves_like_opcodes(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        overall_count = 0
        all_lines = f.readlines()
        for i in range(0, len(all_lines), 4):
            before = literal_eval(all_lines[i].strip().split(': ')[1])
            instruction = [int(j) for j in all_lines[i + 1].strip().split()]
            after = literal_eval(all_lines[i + 2].strip().split(':  ')[1])

            count_three = 0
            for operation in all_operations:
                if operation(before, instruction) == after:
                    count_three += 1
                if count_three == 3:
                    overall_count += 1
                    break

    return overall_count


if __name__ == '__main__':
    overall_count = behaves_like_opcodes('input-1.txt')
    print(overall_count)
