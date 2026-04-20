from functools import wraps
from flask import request, jsonify

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Here you would typically get the user's role from the session or token
            user_role = request.headers.get('Role')  # Example: Get role from request headers
            
            if user_role != required_role:
                return jsonify({'message': 'Access denied: insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator