class NFA:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q # Set of states
        self.Sigma = Sigma # Set of alphabet symbols
        self.delta = delta # Transition relation
        self.q0 = q0 # Start state
        self.F = F # Set of accept states

    def traverse_epsilons(self, states):
        closure = states
        stack = [state for state in states]
        while (len(stack) > 0):
            q = stack.pop()
            epsilon_moves = self.delta.get((q, ""), None)
            if epsilon_moves != None:
                for move in epsilon_moves:
                    if move not in closure:
                        closure.add(move)
                        stack.append(move)
        return closure

    def transition(self, states, symbol):
        outputs = set()
        for state in states:
            try:
                outputs =  outputs | self.delta[(state, symbol)]
            except KeyError:
                outputs = outputs | set()
        return outputs
        
    def run(self, s):
        q = self.traverse_epsilons({self.q0})
        while(s != ""):
            q = self.traverse_epsilons(self.transition(q, s[0]))
            s = s[1:]
        return q & set(self.F) != set()
    
    def describe(self):
        print(self.Q)
        print(self.Sigma)
        print(self.delta)
        print(self.q0)
        print(self.F)

    # Union
    def union(n1, n2):
        new_start = -1
        delta = {(new_start, "") : {n1.q0, n2.q0}} | n1.delta | n2.delta
        return NFA(n1.Q | n2.Q | {new_start}, n1.Sigma | n2.Sigma, delta, new_start, n1.F + n2.F)

    # Concatenation
    def concatenate(self, n2):
        delta = {} | self.delta | n2.delta
        for state in self.F:
            if delta.get((state, "")) != None:
                delta[(state, "")] = delta[(state, "")] | {n2.q0}
            else:
                delta[(state, "")] = {n2.q0}
        return NFA(self.Q | n2.Q, self.Sigma | n2.Sigma, delta, self.q0, n2.F)

    # Kleene Star
    def star(self):
        new_start = -1
        delta = {} | self.delta
        for state in self.F:
            if delta.get((state, "")) != None:
                delta[(state, "")] = delta[(state, "")] | {self.q0}
            else:
                delta[(state, "")] = {self.q0}
            delta[(new_start, "")] = {self.q0}
        return NFA(self.Q | {new_start}, self.Sigma, delta, new_start, self.F + [new_start])


n1 = NFA({0, 1}, 
         {'a', 'b'},
         {(0, 'a'): {0, 1}, (0, 'b'): {1}, (1, 'a'): {2}, (1, 'a'): {3}},
         0,
         [1, 3]
)

delta1 = {
    (0, ""): {1},
    (1, ""): {2},
    (2, "c"): {2}
}

n2 = NFA(
    Q={0, 1, 2},
    Sigma={'c'},
    delta=delta1,
    q0=0,
    F=[2]
)

# print(n2.run("")) # True
# print(n2.run("a")) # True
# print(n2.run("aa")) # True
# print(n2.run("b")) # False

delta2 = {
    (3, "b") : {3},
    (3, "a") : {4},
    (4, "a") : {3},
    (4, "b") : {4}
}

n3 = NFA(Q={3,4},
         Sigma={'a', 'b'},
         delta=delta2,
         q0=3,
         F=[3]
)

n4 = NFA.union(n2, n3)

# n4.describe()
# print(n4.run("aaaaaaa")) # True
# print(n4.run("bbb")) # True
# print(n4.run("ba")) # False

n5 = n2.concatenate(n3)
# n5.describe()

# print(n5.run("caaab")) # False
# print(n5.run("aabbbc")) # False 
# print(n5.run("ccccccccccccccccccccccccccccccccccccccccaa")) # True

delta3 = {(0, 'a') : {1},
          (0, 'c') : {2}, 
          (1, 'b') : {2}

}

n6 = NFA(Q={0,1,2},
         Sigma={'a', 'b', 'c'},
         delta=delta3,
         q0=0,
         F=[2]
)

print("------------ Before Star ------------")
print("abb: " + str(n6.run("abb"))) # False
print("ab: "+ str(n6.run("ab"))) # True
print("c: " + str(n6.run("c"))) # True
print("abc: " + str(n6.run("abc"))) # False

n7 = n6.star()

print("------------ After Star ------------")
print("abb: " + str(n7.run("abb"))) # True
print("ab: "+ str(n7.run("ab"))) # True
print("c: " + str(n7.run("c"))) # True
print("abc: " + str(n7.run("abc"))) # True