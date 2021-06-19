import os

from flask import Flask, jsonify, request

from glop_solver import solve_problem

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'OK', 'status': 200})


@app.route('/solve', methods=['POST'])
def solve():
    # TODO :
    #   - check params
    #   - call solver
    #   - return response json
    objectives = request.json['objectives']
    constraints = request.json['constraints']
    solution = solve_problem(objectives, constraints)
    # print('solution : %s' % solution)
    return jsonify({'message': 'OK', 'status': 200, 'data': solution})
