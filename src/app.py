from flask import Flask, request, jsonify
import os
from functools import wraps
import uuid
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# API Key requerida - DEL EJERCICIO
API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-change-in-production')

def require_api_key(f):
    """Middleware para validar API Key y JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-Parse-REST-API-Key')
        jwt_token = request.headers.get('X-JWT-KWV')
        
        # Validar API Key
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Unauthorized - Invalid API Key"}), 401
            
        # Validar presencia de JWT (en producción se validaría firma)
        if not jwt_token:
            return jsonify({"error": "JWT token required"}), 401
            
        return f(*args, **kwargs)
    return decorated

@app.route('/DevOps', methods=['POST'])
@require_api_key
def devops_endpoint():
    """Endpoint principal del ejercicio"""
    try:
        # Validar que es JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        
        # Validar campos requeridos EXACTAMENTE como en el PDF
        required_fields = ['message', 'to', 'from', 'timeToLifeSec']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Validar tipos de datos
        if not isinstance(data['timeToLifeSec'], int):
            return jsonify({"error": "timeToLifeSec must be an integer"}), 400
        
        # Simular procesamiento con timeToLifeSec
        # En un caso real, podríamos usar esto para programar tareas
        if data['timeToLifeSec'] > 0:
            logger.info(f"Message will live for {data['timeToLifeSec']} seconds")
        
        # Respuesta EXACTA como en el PDF
        response = {
            "message": f"Hello {data['to']} your message will be send"
        }
        
        # Generar JWT único para la transacción (simulado)
        transaction_id = str(uuid.uuid4())
        # En producción: generar JWT real con expiración
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Invalid request format"}), 400

@app.route('/DevOps', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@require_api_key
def other_methods():
    """Para otros métodos HTTP - retorna ERROR como pide el PDF"""
    return "ERROR", 405

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para health checks y load balancer"""
    return jsonify({
        "status": "healthy",
        "service": "devops-microservice",
        "timestamp": time.time(),
        "version": "1.0.0"
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)