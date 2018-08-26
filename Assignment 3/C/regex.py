from Automata import Automata

def main(inputfile):
    alphabet = []
    regex = ""
    input_string = ""
    with open(inputfile, 'rU') as f:
        alphabet = f.readline().rsplit()
        regex = str(f.readline().rstrip())
        input_string = str(f.readline().rstrip())

    postfix = infixToPostfix(regex)
    stack = []
    for char in postfix:
        if char in alphabet:
            stack.append(basicMachine(char)) # push basic machine to stack
        if char == '|':
            if len(stack) < 2:
                raise BaseException("Error processing operator '|'. Inadequate operands")
            b = stack.pop()
            a = stack.pop()
            stack.append(unionMachine(a,b)) # pop two machines from stack and push their union
        if char == '*':
            if len(stack) < 1:
                raise BaseException("Error processing operator '*'. Inadequate operands")
            a = stack.pop()
            stack.append(starMachine(a)) # pop one machine from stack and push it's closure
        if char == '.':
            if len(stack) < 2:
                raise BaseException("Error processing operator '.'. Inadequate operands")
            b = stack.pop()
            a = stack.pop()
            stack.append(dotMachine(a,b)) # pop two machines from stack and push their concatenation

    if len(stack) > 1: # final automata
        raise BaseException("Error.")
    checkMember(stack.pop(), input_string)

# check if input string belongs to an NFA's language
def checkMember(NFA, input_string):
    current_state = NFA.initial
    new_states = NFA.eClose(set([current_state]))
    for char in input_string:
        new_states = NFA.eClose(NFA.getTransitions(new_states, char))
    if NFA.final[0] in new_states:
        print "Yes."
    else:
        print "No."

# For building automata, I have used Thompson's construction (https://en.wikipedia.org/wiki/Thompson%27s_construction)
# instead of the approach we took in class because there will always be a single final state, and is therefore easier to handle.

# simplest automata with two states
def basicMachine(char):
    state1 = 1
    state2 = 2
    auto = Automata()
    auto.setInitialState(state1)
    auto.addFinalStates(state2)
    auto.addTransition(state1, state2, char)
    return auto

# union of two automata
def unionMachine(a,b):
    a, n1 = a.rebuild(2) # rename the states to accomodate the new start and final states
    b, n2 = b.rebuild(n1) # 'b' is an automata and 'n2' is the last state name(number) of 'b'
    state1 = 1
    state2 = n2
    auto = Automata()
    auto.setInitialState(state1) # new initial state
    auto.addFinalStates(state2) # new final state
    auto.addTransition(auto.initial, a.initial, ":e:") # :e: = epsilon, e-transition from new starting state to original starting states
    auto.addTransition(auto.initial, b.initial, ":e:")
    auto.addTransition(a.final[0], auto.final[0], ":e:") # e-transition from original final states to new final state
    auto.addTransition(b.final[0], auto.final[0], ":e:")
    auto.addTransitionTable(a.transitions) # add original transitions
    auto.addTransitionTable(b.transitions)
    return auto

# closure of an automata
def starMachine(a):
    a, n1 = a.rebuild(2)
    state1 = 1
    state2 = n1
    auto = Automata()
    auto.setInitialState(state1)
    auto.addFinalStates(state2)
    auto.addTransition(auto.initial, a.initial, ":e:")
    auto.addTransition(auto.initial, auto.final[0], ":e:") # e-transition from initial state to final state for empty string
    auto.addTransition(a.final[0], auto.final[0], ":e:")
    auto.addTransition(a.final[0], a.initial, ":e:") # e-transition from old final state to old initial state for loop
    auto.addTransitionTable(a.transitions)
    return auto

# concatenate two automata
def dotMachine(a,b):
    a, n1 = a.rebuild(1)
    b, n2 = b.rebuild(n1)
    state1 = 1
    state2 = n2-1
    auto = Automata()
    auto.setInitialState(state1)
    auto.addFinalStates(state2)
    auto.addTransition(a.final[0], b.initial, ":e:") # e-transition from a's final state to b's initial state
    auto.addTransitionTable(a.transitions)
    auto.addTransitionTable(b.transitions)
    return auto

# convert the regex to an easily readable postfix format
# reference: https://codereview.stackexchange.com/questions/116974/infix-to-postfix-implementation-using-a-stack
def infixToPostfix(infix):
    operators  = {"|": 1, ".": 2, "*": 3}
    brackets = set(["(", ")"])
    stack = []
    postfix = []
    for c in infix:
        if c in operators:
            if stack:
                top = stack[-1]
                while top in operators and operators[top] >= operators[c]:
                    postfix.append(stack.pop())
                    if stack:
                        top = stack[-1]
                    else:
                        break
            stack.append(c)
        elif c in brackets:
            if c == ")":
                try:
                    while stack[-1] != "(":
                        postfix.append(stack.pop())
                except IndexError:
                    raise ValueError("'(' not found when popping")
                stack.pop()
            else:
                stack.append(c)
        else:
            postfix.append(c)
    postfix.extend(token for token in reversed(stack) if token in operators)
    return postfix

# run. enter input file name as parameter
main("input.txt")
