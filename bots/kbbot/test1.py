import sys
from kb import KB, Boolean, Integer, Constant

# Define our symbols
Q = Boolean('Q')
P = Boolean('P')
R = Boolean('R')

# Create a new knowledge base
kb = KB()

# Add clauses
kb.add_clause(P, Q)
kb.add_clause(~Q, R)
kb.add_clause(~R, ~P)
kb.add_clause(Q, ~P)
kb.add_clause(P,~Q)

# Print all models of the knowledge base
for model in kb.models():
    print(model)

# Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print(kb.satisfiable())
