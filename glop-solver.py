import json
import sys

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


def get_json_from_file(file_path):
    try:
        with open(file_path, 'r') as fd:
            json_decoded = json.load(fd)
            for key in ["objectives", "constraints"]:
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


def main(file_path):
    json_content = get_json_from_file(file_path)

    solution = solve_problem(json_content['objectives'], json_content['constraints'])

    json_content['solution'] = solution

    write_json_to_file(file_path, json_content)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Need at least one arg")
        exit(1)
    if len(sys.argv) > 2:
        print("Too many args")
        exit(1)

    main(sys.argv[1])
