# to run 3A or 3B edit lines 178 and 181 respectively
# then, execute python convert.py

import re
from graphviz import Digraph
from copy import deepcopy

# 3A. convert NFA to DFA, save to file and draw diagram
def convertToDFA(input_file, output_file):

    NFA = getNFA(input_file)

    DFA = reduceDFA(getDFA(NFA))

    # write DFA to file
    writeDFA(DFA, output_file)
    # draw DFA diagram
    drawDFA(DFA)

# 3B. check if a string is valid for an NFA's language
def checkMember(NFA_file, string_file):
    NFA = getNFA(NFA_file)
    d_states, d_initial, d_final, d_transition = getDFA(NFA)

    string = open(string_file, 'r').readline().rstrip()

    current_state = d_initial

    for i in string:
        current_state = d_transition[current_state][int(i)]

    if current_state in d_final:
        print "Yes."
    else:
        print "No."

# write DFA to file
def writeDFA(DFA, output_file):
    d_states, d_initial, d_final, d_transition = DFA

    with open(output_file, 'w') as f:
        # state set
        for i in d_states:
            if i == []:
                f.write("{} ")
            else:
                f.write("{" + ",".join(list(i)) + "} ")
        f.write("\n")
        # starting state
        f.write("{" + ",".join(list(d_initial)) + "}\n")
        # final states
        for i in d_final:
            if i == []:
                f.write("{} ")
            else:
                f.write("{" + ",".join(list(i)) + "} ")
        f.write("\n")
        # transition table
        for i in d_states:
            f.write(re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(d_transition[frozenset(i)][0]))))) + " " + re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(d_transition[frozenset(i)][1]))))) + "\n")

# use graphviz library to draw diagram of DFA
def drawDFA(DFA):
    d_states, d_initial, d_final, d_transition = DFA

    f = Digraph('finite_state_machine', filename='DFA.gv')
    f.attr(rankdir='LR')

    f.attr('node', shape='doublecircle')
    for i in d_final:
        f.node(re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(i))))))

    f.attr('node', shape='diamond')
    f.node(re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(d_initial))))))

    f.attr('node', shape='circle')

    for i in d_states:
        f.edge(re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(i))))), re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(d_transition[frozenset(i)][0]))))), label='0')
        f.edge(re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(i))))), re.sub('[]]', '}', re.sub('[[]', '{', re.sub("[']", '', str(list(d_transition[frozenset(i)][1]))))), label='1')
    f.view()

# partially reduce DFA to make comprehension easier
def reduceDFA(DFA):
    d_states, d_initial, d_final, d_transition = DFA

    # at least one state transitions to the following states
    acpt_states = list(set([state for pair in d_transition.values() for state in pair]))
    new_states = deepcopy(d_states)
    new_final = deepcopy(d_final)
    new_transition = deepcopy(d_transition)

    for i in d_states:
        if i not in acpt_states and i != d_initial:
            if i in new_final:
                new_final.remove(i)
            del new_transition[i]
            new_states.remove(i)

    return new_states, d_initial, new_final, new_transition

# generate DFA from NFA
def getDFA(NFA):
    n_states, n_initial, n_final, n_transition = NFA

    d_states = powerset(n_states)
    for i in range(0, len(d_states)):
        d_states[i] = frozenset(d_states[i])
    d_initial = frozenset(eclose(n_initial, n_transition))
    d_final = intersect(n_final, d_states)
    d_transition = {frozenset(i): [] for i in d_states}

    # populating DFA's transition table
    for i in d_states:
        if i == []:
            d_transition[frozenset()] = [frozenset([]), frozenset([])]
            continue
        for j in range(0, 2):
            temp = []
            for k in i:
                temp.extend(n_transition.get(int(re.findall('\d+', k)[0]))[j])
            close = eclose(temp, n_transition)
            d_transition[frozenset(i)].append(frozenset(close))

    return d_states, d_initial, d_final, d_transition

# read NFA from file
def getNFA(input_file):
    n_states = []
    n_initial = []
    n_final = []
    n_transition = {}

    with open(input_file, 'rU') as f:
        n_states.extend([state for state in f.readline().rsplit()])
        n_initial.extend([state for state in f.readline().rsplit()])
        n_final.extend([state for state in f.readline().rsplit()])
        index = 0
        for line in f:
            temp = line.rsplit()
            n_transition[index] = []
            for i in temp:
                j = re.sub('[{}]', '', str(i))
                n_transition[index].append([] if j == '' else j.split(","))
            index += 1

    return n_states, n_initial, n_final, n_transition

# power set
def powerset(inp):
    size = len(inp)
    power = []
    for i in range(1 << size):
        power.append([inp[j] for j in range(0, size) if (i & (1 << j))])
    return power

# eclose of a state in NFA
def eclose(inp, n_transition):
    inp = list(inp)
    if inp == []: # empty set
        return []
    elif len(inp) == 1:
        # union of singleton set and its eclose
        return list(set().union(n_transition[int(re.findall('\d+', inp[0])[0])][2], inp))
    else:
        # union of eclose of all elements
        return list(set().union(eclose([inp[0]], n_transition), (eclose(inp[1:], n_transition))))

# intersection of sets
def intersect(n_final, d_states):
    final = []
    for state_set in d_states:
        # all sets with at least one state in final state of NFA
        if [value for value in state_set if value in n_final] != []:
            final.append(frozenset(state_set))
    return final

# 3A. convert NFA to DFA, save to file and draw diagram
convertToDFA("NFA.txt", "DFA.txt")

# 3B. check if a string is valid for an NFA's language
checkMember("NFA.txt", "input-string.txt")
