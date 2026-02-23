import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import os

def generate_jwt(payload_data, secret=None, expires_in=3600):
    """Genera un JWT token"""
    if secret is None:
        secret = os.getenv('JWT_SECRET', 'dev-secret')
    
    payload = {
        **payload_data,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
        'iat': datetime.datetime.utcnow(),
        'iss': 'devops-microservice'
    }
    
    return jwt.encode(payload, secret, algorithm='HS256')

def validate_jwt(token, secret=None):
    """Valida y decodifica un JWT token"""
    if secret is None:
        secret = os.getenv('JWT_SECRET', 'dev-secret')
    
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'], issuer='devops-microservice')
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError as e:
        return {"error": f"Invalid token: {str(e)}"}
    except Exception as e:
        return {"error": f"Token validation error: {str(e)}"}

def jwt_required(f):
    """Decorator para endpoints que requieren JWT válido"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-JWT-KWV')
        
        if not token:
            return jsonify({"error": "JWT token required"}), 401
        
        validation_result = validate_jwt(token)
        if "error" in validation_result:
            return jsonify({"error": validation_result["error"]}), 401
        
        # Agregar payload del JWT al request para uso en la función
        request.jwt_payload = validation_result
        
        return f(*args, **kwargs)
    return decorated