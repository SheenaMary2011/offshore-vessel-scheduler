from ortools.sat.python import cp_model

model = cp_model.CpModel()            # 1. an empty "question sheet"

x = model.new_int_var(1, 10, "x")     # 2. an unknown: a number from 1 to 10

model.add(x != 9)                     # 3. a rule
model.maximize(x)                     # 4. the goal

solver = cp_model.CpSolver()          # the "engine" that answers the question sheet
solver.solve(model)
print(solver.value(x))                # read the answer