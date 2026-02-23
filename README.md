# DevOps Microservice - Banco Pichincha

Microservicio REST para evaluación técnica DevOps con Python, Docker, Kubernetes y CI/CD.

## 🚀 Características

- ✅ Endpoint `/DevOps` con método POST
- ✅ Autenticación con API Key y JWT
- ✅ Containerizado con Docker
- ✅ Configuración para Kubernetes
- ✅ Pipeline CI/CD con GitHub Actions
- ✅ Pruebas unitarias con cobertura >80%
- ✅ Código limpio y formateado

## 📋 Requisitos del Ejercicio

### Endpoint Principal
- **URL**: `/DevOps`
- **Método**: POST
- **Headers**:
  - `X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c`
  - `X-JWT-KWV: <jwt_token>`
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45
  }