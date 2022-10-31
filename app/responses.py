from flask import jsonify

def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def conflict(message):
    response = jsonify({'error': 'conflict', 'message': message})
    response.status_code = 409
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def success(result, status_code=200, message="Success"):
    response = jsonify({'result': result, "message": message})
    response.status_code=status_code
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def not_found(status_code=404):
    response = jsonify({'message': "not found"})
    response.status_code=status_code
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
