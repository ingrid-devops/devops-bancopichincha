# test_endpoint.py
import requests
import json

print("🧪 Probando endpoint /DevOps...")

headers = {
    'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
    'X-JWT-KWV': 'test-jwt-12345',
    'Content-Type': 'application/json'
}

data = {
    'message': 'This is a test',
    'to': 'Juan Perez',
    'from': 'Rita Asturia',
    'timeToLifeSec': 45
}

try:
    response = requests.post('http://localhost:5000/DevOps', headers=headers, json=data)
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response: {response.json()}")
    
    # Verificar que la respuesta es EXACTAMENTE lo que pide el PDF
    expected_response = {"message": "Hello Juan Perez your message will be send"}
    actual_response = response.json()
    
    if actual_response == expected_response:
        print("🎯 ¡RESPUESTA CORRECTA! Coincide con lo requerido en el PDF")
    else:
        print("⚠️  La respuesta NO coincide exactamente con lo requerido")
        print(f"   Esperado: {expected_response}")
        print(f"   Obtenido: {actual_response}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Asegúrate de que el servidor esté ejecutándose en otra terminal")