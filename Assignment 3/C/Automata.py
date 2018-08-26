class Automata:
    def __init__(self):
        self.states = set()
        self.initial = None
        self.final = []
        self.transitions = dict() # {start: {end1:key1, end2:key2}}

    # set the initial state of the automata
    def setInitialState(self, state):
        self.initial = state
        self.states.add(state)

    # add a final state to the automata
    def addFinalStates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.final:
                self.final.append(s)

    # add a transition to the automata's transition table
    def addTransition(self, start, end, key):
        if isinstance(key, str):
            key = set([key])
        self.states.add(start)
        self.states.add(end)
        if start in self.transitions:
            if end in self.transitions[start]:
                self.transitions[start][end] = self.transitions[start][end].union(key)
            else:
                self.transitions[start][end] = key
        else:
            self.transitions[start] = {end : key}

    # add all transitions from another table to the automata's table
    def addTransitionTable(self, transitions):
        for start, end in transitions.items():
            for state in end:
                self.addTransition(start, state, end[state])

    # get all states that can be reached from a state without any e-transitions
    def getTransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        toStates = set()
        for each in state:
            if each in self.transitions:
                for trans in self.transitions[each]:
                    if key in self.transitions[each][trans]:
                        toStates.add(trans)
        return toStates

    # rebuild an automata with different state names
    def rebuild(self, starting):
        translations = {}
        for i in list(self.states):
            translations[i] = starting
            starting += 1
        new_machine = Automata()
        new_machine.setInitialState(translations[self.initial])
        new_machine.addFinalStates(translations[self.final[0]])
        for start, end in self.transitions.items():
            for state in end:
                new_machine.addTransition(translations[start], translations[state], end[state])
        ending = starting
        return new_machine, ending

    # get eclose of a state
    def eClose(self, findstate):
        allstates = set()
        states = findstate
        while len(states)!= 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if ":e:" in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates
