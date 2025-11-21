class DFA:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q # Set of states
        self.Sigma = Sigma # Set of alphabet symbols
        self.delta = delta # Transition function --> d(state, symbol) = symbol
        self.q0 = q0 # Start state
        self.F = F # Set of accept states

    def run(self, s):
        q = self.q0 
        while(s != ""):
            q = self.delta[(q, s[0])]
            s = s[1:]
        return q in self.F

m1 = DFA({0, 1}, 
         {"a", "b"},  
         {(0, 'a'):0, (0, 'b'):1, (1, 'a'):0, (1, 'b'):1}, 
         1, 
         [1])

def main():
    print(m1.run("abba"))
    print(m1.run("abb"))
    print(m1.run("abbaa"))

main()