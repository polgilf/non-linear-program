from pyomo.environ import *


# Create the model
model = ConcreteModel()

# Variables
model.p1 = Var(bounds=(0, 10000/8), doc='Price of product 1')
model.p2 = Var(bounds=(0, 16000/10), doc='Price of product 2')
model.q1 = Var(bounds=(0, None), doc='Quantity of product 1')
model.q2 = Var(bounds=(0, None), doc='Quantity of product 2')

# Constraints
def demand1_rule(model):
    return model.q1 == 10000 - 8*model.p1
model.demand1 = Constraint(rule=demand1_rule)

def demand2_rule(model):
    return model.q2 == 16000 - 10*model.p2
model.demand2 = Constraint(rule=demand2_rule)

def machine_hours_rule(model):
    return 0.1*model.q1 + 0.2*model.q2 <= 600
model.machine_hours = Constraint(rule=machine_hours_rule)

def raw_material_rule(model):
    return 0.5*model.q1 + 0.3*model.q2 <= 3000
model.raw_material = Constraint(rule=raw_material_rule)

# Objective
def profit_rule(model):
    revenue = model.p1*model.q1 + model.p2*model.q2
    costs = 2000*(0.1*model.q1 + 0.2*model.q2) + 500*(0.5*model.q1 + 0.3*model.q2)
    return revenue - costs
model.profit = Objective(rule=profit_rule, sense=maximize)

# Solve
solver = SolverFactory('ipopt')
results = solver.solve(model)

# Print results
if results.solver.status == SolverStatus.ok:
    print(f"Optimal p1: {value(model.p1):.2f}")
    print(f"Optimal p2: {value(model.p2):.2f}")
    print(f"Optimal q1: {value(model.q1):.2f}")
    print(f"Optimal q2: {value(model.q2):.2f}")
    print(f"Maximum profit: {value(model.profit):.2f}")