from nocktensors.interface import nock, print_noun
from nocktensors.interpreter import nock_interpreter
from nocktensors.utils import create_noun

def demo_op0_slot():
    # *[ [4 5] [0 2] ] → 4
    print("op0: slot")
    subject = [4, 5]
    formula = [0, 2]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op1_constant():
    # *[ 42 [1 3] ] → 3
    print("op1: constant")
    subject = 42
    formula = [1, 3]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op2_compose():
    # *[ 42 [2 [1 5] [1 6]] ] → [5, 6]
    print("op2: compose")
    subject = 42
    formula = [2, [1, 5], [1, 6]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op3_is_cell():
    # *[ [4 5] [3 [0 1]] ] → 0
    print("op3: is cell")
    subject = [4, 5]
    formula = [3, [0, 1]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op4_increment():
    # increment an atom
    print("op4: increment")
    subject = 7
    formula = [4, [0, 1]]  # +*[ 7 [0 1] ] should yield 8
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_all():
    print(" ███▄    █  ▒█████   ▄████▄   ██ ▄█▀▄▄▄█████▓▓█████  ███▄    █   ██████  ▒█████   ██▀███    ██████\n██ ▀█   █ ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓  ██▒ ▓▒▓█   ▀  ██ ▀█   █ ▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▒██    ▒ \n▓██  ▀█ ██▒▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██  ▀█ ██▒░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒░ ▓██▄   \n▓██▒  ▐▌██▒▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▓██▒  ▐▌██▒  ▒   ██▒▒██   ██░▒██▀▀█▄    ▒   ██▒\n▒██░   ▓██░░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██░   ▓██░▒██████▒▒░ ████▓▒░░██▓ ▒██▒▒██████▒▒\n░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░\n░ ░░   ░ ▒░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░    ░     ░ ░  ░░ ░░   ░ ▒░░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒  ░ ░\n░   ░ ░ ░ ░ ░ ▒  ░        ░ ░░ ░   ░         ░      ░   ░ ░ ░  ░  ░  ░ ░ ░ ▒    ░░   ░ ░  ░  ░  \n░     ░ ░  ░ ░      ░  ░               ░  ░         ░       ░      ░ ░     ░           ░  \n░")
    print("=" * 40)
    demo_op0_slot()
    demo_op1_constant()
    demo_op2_compose()
    demo_op3_is_cell()
    demo_op4_increment()

def main():
    demo_all()

if __name__ == "__main__":
    main()
