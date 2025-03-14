import sys

from permutation import permutate
from template import description, head, tail


label = 0


def next_label():
    global label
    label += 1
    return f"label_{label}"


# transitions for [5,6,7] [8,9]
# [5, 6, 7, 8, 9],
# [5, 6, 8, 7, 9],
# [5, 6, 8, 9, 7],
# [5, 8, 6, 7, 9],
# [5, 8, 6, 9, 7],
# [5, 8, 9, 6, 7],
# [8, 5, 6, 7, 9],
# [8, 5, 6, 9, 7],
# [8, 5, 9, 6, 7],
# [8, 9, 5, 6, 7],


# filter transitions[0] == i
# eg: if i == 5, it returns
# [5, 6, 7, 8, 9]
# [5, 6, 8, 7, 9]
# [5, 6, 8, 9, 7]
# [5, 8, 6, 7, 9]
# [5, 8, 6, 9, 7]
# [5, 8, 9, 6, 7]
def filter(transitions, i):
    filtered_arrays = [arr for arr in transitions if arr[0] == i]
    return filtered_arrays


# return [5, 8]
def possible_branches(transitions):
    unique_items = {arr[0] for arr in transitions}
    ret = list(unique_items)
    ret.sort()
    return ret


def save_to_memory(is_last_round, n, offset):
    if is_last_round:
        print(f"{hex((offset)*0x20)} mstore")
    else:
        print("msize mstore")


def build_return(n, is_last_round):
    if not is_last_round:
        for i in range(0, n):
            save_to_memory(False, 0, 0)

    print("msize 0x0 return")


def build_if_block(n, transitions1, transitions2, offset, beg1, beg2, label_exit):
    label = next_label()

    is_last_round = n >= 8
    # dir = "gt" if is_last_round else "lt"
    dir = "lt"

    ofst = 0 if is_last_round else offset

    if n == 2:  # optimize for 2 numbers, simplify it to:
        #   x, y
        #   if x>y
        #     swap1
        print(f"dup{ofst+beg1+1} dup{ofst+beg2+2} // x, y")
        print(f"dup2 dup2 {dir} {label} jumpi // if x<y")
        print("swap1")
        print(f"{label}: // if x>y")
    else:
        print(f"dup{ofst+beg1+1} dup{ofst+beg2+2} {dir} {label} jumpi // if x<y")
        print(f"dup{ofst+beg1+1} // move x to stack top")
        if is_last_round:
            save_to_memory(is_last_round, n, offset)

        build_block(
            n,
            [sublist[1:] for sublist in transitions1],
            offset + 1,
            label_exit,
        )

        print(f"{label}: // if x>y")
        print(
            f"dup{ofst+beg2+1} // move y to stack top, offset: {offset}, beg2: {beg2}"
        )
        if is_last_round:
            save_to_memory(is_last_round, n, offset)
        build_block(
            n,
            [sublist[1:] for sublist in transitions2],
            offset + 1,
            label_exit,
        )


def build_single_block(n, transitions, offset, label_exit):
    is_last_round = n >= 8
    ofst = 0 if is_last_round else offset

    if len(transitions) == 1:  # must be 1
        tr = transitions[0]

        #              3 2 1 [4 5 6]
        # i=0        4 3 2 1 [4 5 6]
        # i=1      5 4 3 2 1 [4 5 6]
        # i=2    6 5 4 3 2 1 [4 5 6]

        # [2, 4, 5, 9, 22, 1, 4, 8, 33, 99]
        for i in tr:
            print(
                f"dup{ofst+1+i} //*i:{i} offset:{offset} transitions: {transitions}*/"
            )
            if is_last_round:
                save_to_memory(is_last_round, n, offset)
                offset += 1
            else:
                ofst += 1

    if is_last_round:
        build_return(n, is_last_round)

    elif label_exit != "":
        print(f"{label_exit} jump // end of 1 transition")


def build_block(n, transitions, offset, label_exit):
    branches_ = possible_branches(transitions)  # e.g.: [5, 8]

    if len(branches_) == 2:
        x, y = branches_[0], branches_[1]
        build_if_block(
            n, filter(transitions, x), filter(transitions, y), offset, x, y, label_exit
        )
    else:
        build_single_block(n, transitions, offset, label_exit)


# reverse the order of the top n numbers.
def swap(n):
    if n == 5:
        print("swap4 swap3 swap1 swap3")
    elif n == 3:
        print("swap2")
    elif n == 2:
        print("swap1 // swap n=2")
    elif n == 4:
        print("swap3 swap2 swap1 swap2 //swap n==4")
    else:
        raise RuntimeError("unknown n...............")


# -------------- test cases --------------
# print("0xa 0x8 0x6 0x4 0x2 0x9 0x7 0x5 0x3 0x1")
# on stack
# 0x10 0x30 0x50 0x70 0x90 0x20 0x40 0x60 0x80 0xa0 ]

# beg1, end1, beg2, end2 = 6, 6, 7, 7 # 1*1
# beg1, end1, beg2, end2 = 0, 1, 2, 2 # 2*1
# print("0x20 0x33 0x10")
# beg1, end1, beg2, end2 = 0, 1, 2, 2 # 2*1
# print("0x10 0x33 0x20")
# beg1, end1, beg2, end2 = 0, 2, 3, 3  # 3*1
# print("0x40 0x33 0x20 0x10")
# beg1, end1, beg2, end2 = 0, 0, 1, 3  # 1*3
# print("0x40 0x20 0x10 0x30")
# beg1, end1, beg2, end2 = 0, 2, 3, 4  # 3*2
# print("0x50 0x30 0x60 0x40 0x20")
# beg1, end1, beg2, end2 = 0, 3, 4, 7  # 4*4
# beg1, end1, beg2, end2 = 0, 4, 5, 9  # all 10 numbers

# transitions = permutate(beg1, end1, beg2, end2)
# # label_exit = next_label()
# label_exit = ""
# build_block(transitions, offset=0, label_exit=label_exit)
# if label_exit != "":
#     print(f"{label_exit}:")
# swap(end2 - beg1 + 1)


# ---------------- start ----------------
lv2 = "./src/Lv2.huff"
with open(lv2, "w"):  # clear previous
    pass

sys.stdout = open(lv2, "a")  # redirect print() to file


print(description)
print(head)


# round 1
#   x0, x1, x2, x3, x4, x5, x6, x7, x8, x9
# ->
#   [x0, x1] [x2] [x3, x4] [x5, x6] [x7] [x8, x9]
for i in range(0, 2):
    # process [x8, x9]
    beg1, end1, beg2, end2 = 8, 8, 9, 9  # last 2
    n = end2 - beg1 + 1
    transitions = permutate(beg1, end1, beg2, end2)
    build_block(n, transitions, 0, "")

    # process [x7]
    print("dup10")

    # process [x5, x6]
    beg1, end1, beg2, end2 = 8, 8, 9, 9  # last 2
    n = end2 - beg1 + 1
    transitions = permutate(beg1, end1, beg2, end2)
    build_block(n, transitions, 0, "")

# round 2
#   [x0, x1] [x2] [x3, x4] [x5, x6] [x7] [x8, x9]
# ->
#   [x0, x1, x2] [x3, x4] [x5, x6, x7] [x8, x9]
for i in range(0, 2):
    # [x8, x9]
    print("dup10 dup10")

    # [x5, x6, x7]
    beg1, end1, beg2, end2 = 7, 8, 9, 9
    n = end2 - beg1 + 1
    transitions = permutate(beg1, end1, beg2, end2)
    label_exit = next_label()
    build_block(n, transitions, 0, label_exit)
    print(f"{label_exit}:")
    swap(n)

# # round 3
# #   [x0, x1, x2] [x3, x4] [x5, x6, x7] [x8, x9]
# # ->
# #   [x0, x1, x2, x3, x4] [x5, x6, x7, x8, x9]
for i in range(0, 2):
    beg1, end1, beg2, end2 = 5, 7, 8, 9
    n = end2 - beg1 + 1
    transitions = permutate(beg1, end1, beg2, end2)
    label_exit = next_label()
    build_block(n, transitions, 0, label_exit)
    print(f"{label_exit}:")
    swap(n)

# for dubugging, locating the last round in the playground
# print("0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1")
# print("0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1")
# print("0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1")
# print("0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1")
# print("0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1 0x1")
# print("pop pop pop pop pop pop pop pop pop pop pop")
# print("pop pop pop pop pop pop pop pop pop pop pop")
# print("pop pop pop pop pop pop pop pop pop pop pop")
# print("pop pop pop pop pop pop pop pop pop pop pop")
# print("pop pop pop pop pop pop pop pop pop pop pop")

# round 4
#   [x0, x1, x2, x3, x4] [x5, x6, x7, x8, x9]
# ->
#   [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9]
beg1, end1, beg2, end2 = 0, 4, 5, 9
n = end2 - beg1 + 1
transitions = permutate(beg1, end1, beg2, end2)
label_exit = next_label()
build_block(n, transitions, 0, label_exit)
print(f"{label_exit}:")

print(tail)
