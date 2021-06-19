from ortools.linear_solver import pywraplp


def solve_problem(objectives_list, constraint_list):
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    objectives_dict = {i: objectives_list[i] for i in range(0, len(objectives_list))}

    vars_list = {}
    for idx, item in objectives_dict.items():
        vars_list[idx] = (solver.IntVar(0, solver.infinity(), str(idx)))

    for constraint in constraint_list:
        calc = None
        for idx, obj in objectives_dict.items():
            if calc is None:
                calc = (constraint.get("coefficients")[idx] * vars_list[idx])
            else:
                calc += (constraint.get("coefficients")[idx] * vars_list[idx])

        solver.Add(calc == constraint.get("value"))

    objective = solver.Objective()
    for idx, item in objectives_dict.items():
        objective.SetCoefficient(vars_list[idx], item)
    objective.SetMinimization()

    solver.Solve()

    final_solution = {}
    for key, item in vars_list.items():
        final_solution[key] = item.solution_value()

    return final_solution
