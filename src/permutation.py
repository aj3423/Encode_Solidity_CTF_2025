from rich import print

count = 0


def permutate(beg1, end1, beg2, end2):
    list1 = list(range(beg1, end1 + 1))
    list2 = list(range(beg2, end2 + 1))

    def interleave(lst1, lst2):
        global count
        if not lst1:
            return [lst2]
        if not lst2:
            return [lst1]

        results = []
        for tail in interleave(lst1[1:], lst2):
            count += 1
            results.append([lst1[0]] + tail)
        for tail in interleave(lst1, lst2[1:]):
            results.append([lst2[0]] + tail)
        return results

    return interleave(list1, list2)


def generate_transitions(arrays):
    transitions = {}

    for arr in arrays:
        for i in range(len(arr) - 1):
            current = arr[i]
            next_val = arr[i + 1]

            if current not in transitions:
                transitions[current] = set()

            transitions[current].add(next_val)

    for key in transitions:
        transitions[key] = sorted(list(transitions[key]))[:2]

    return transitions


# interleavings = permutate(5, 7, 8, 9)
# # for seq in interleavings:
# #     print(seq)

# transitions = generate_transitions(interleavings)
# print(transitions)
# print("count", count)
