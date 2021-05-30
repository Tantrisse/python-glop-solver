import json
import sys

from ortools.linear_solver import pywraplp


def solve_problem(objectives_dict, constraint_list, lower_bound):
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Create the variables x and y.
    vars_list = {}
    for idx, item in objectives_dict.items():
        vars_list[idx] = (solver.IntVar(0, solver.infinity(), str(idx)))

    # print('Number of variables =', solver.NumVariables())
    for constraint in constraint_list:
        calc = None
        for idx, obj in objectives_dict.items():
            if calc is None:
                calc = (constraint.get("coefficients")[idx] * vars_list[idx])
            else:
                calc += (constraint.get("coefficients")[idx] * vars_list[idx])

        solver.Add(calc == constraint.get("value"))
    # print('Number of constraints =', solver.NumConstraints())

    objective = solver.Objective()
    for idx, item in objectives_dict.items():
        objective.SetCoefficient(vars_list[idx], item)
    objective.SetMinimization()

    solver.Solve()

    # print('Solution:')
    # print('Objective value =', objective.Value())
    final_solution = {}
    for key, item in vars_list.items():
        final_solution[key] = item.solution_value()
        # print(key, '=', item.solution_value())

    return final_solution


def get_json_from_file(file_path):
    try:
        with open(file_path, 'r') as fd:
            json_decoded = json.load(fd)
            for key in ["objectives", "constraints", "lb"]:
                if key not in json_decoded:
                    print('Error while reading the file %s, there is no %s key !' % key)
                    exit(1)
            return json_decoded
    except json.JSONDecodeError:
        print('Error while reading the file %s, it cannot be parsed to Json !' % file_path)
        exit(1)


def write_json_to_file(file_path, data):
    with open(file_path, 'w') as fd:
        json.dump(data, fd, indent=2)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Need at least one arg")
        exit(1)
    if len(sys.argv) > 2:
        print("Too many args")
        exit(1)

    json = get_json_from_file(sys.argv[1])

    solution = solve_problem(json['objectives'], json['constraints'], json['lb'])

    json['solution'] = solution

    write_json_to_file(sys.argv[1], json)

    # objectives = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
    # constraints = [
    #     {
    #         "coefficients": [1, 1, -1, -0, -1, -0],
    #         "value": -11611
    #     },
    #     {
    #         "coefficients": [-1, -0, 1, 1, -0, -1],
    #         "value": 987
    #     },
    #     {
    #         "coefficients": [-0, -1, -0, -1, 1, 1],
    #         "value": 10624
    #     }
    # ]
    # solve_problem(objectives, constraints)
    # test()
