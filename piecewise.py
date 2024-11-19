from docplex.mp.model import Model

n_piecewise = 1250
p1_ub = 10000/8
p2_ub = 16000/10

# Create the model
mdl = Model('revenue_optimization')

# Define price decision variables
p1 = mdl.continuous_var(name='p1', lb=0, ub=10000/8)
p2 = mdl.continuous_var(name='p2', lb=0, ub=16000/10)

# Define quantity decision variables
q1 = mdl.continuous_var(name='q1', lb=0)
q2 = mdl.continuous_var(name='q2', lb=0)

# Define other variables
profit = mdl.continuous_var(name='profit')
income = mdl.continuous_var(name='income')
costs = mdl.continuous_var(name='costs')

# Create piecewise function 1
# Create n_piecewise evenly spaced breakpoints: List of Tuples (x,y): x from 0 to p_ub and y from 0 to x^2
# for p1
break_points1 = [(i, i**2) for i in range(0, int(p1_ub), int(p1_ub/n_piecewise))]
# for p2
break_points2 = [(i, i**2) for i in range(0, int(p2_ub), int(p2_ub/n_piecewise))]

# Piecewise functions for p1^2 and p2^2
piecewise_function1 = mdl.piecewise(0, break_points1, 0)
piecewise_function2 = mdl.piecewise(0, break_points2, 0)

# Constraints
# Define demand constraints
mdl.add_constraint(q1 == 10000 - 8*p1, 'demand1')
mdl.add_constraint(q2 == 16000 - 10*p2, 'demand2')

# Resource constraints
mdl.add_constraint(0.1*q1 + 0.2*q2 <= 600, 'machine_hours')
mdl.add_constraint(0.5*q1 + 0.3*q2 <= 3000, 'raw_material')

# Calculate costs
costs = 2000 * (0.1*q1 + 0.2*q2) + 500 * (0.5*q1 + 0.3*q2)

# Calculate income
income = 10000*p1 - 8*piecewise_function1(p1) + 16000*p2 - 10*piecewise_function2(p2) 

# Profit constraint using piecewise functions
mdl.add_constraint(profit == income - costs)

# Maximize profit
mdl.minimize(-profit)

# Solve the model
solution = mdl.solve(log_output=True)

# Print results
if solution:
    print(f"Optimal p1: {solution.get_value(p1):.2f}")
    print(f"Optimal p2: {solution.get_value(p2):.2f}")
    print(f"Optimal q1: {solution.get_value(q1):.2f}")
    print(f"Optimal q2: {solution.get_value(q2):.2f}")
    print(f"Maximum profit: {-solution.get_objective_value():.2f}")
    print("\n*** REPORT ***\n")
    print(mdl.report())
else:
    print("No solution found")