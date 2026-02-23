.PHONY: help install test lint format build run clean

help:
	@echo "DevOps Microservice - Comandos disponibles:"
	@echo "  install     Instalar dependencias y configurar entorno"
	@echo "  test        Ejecutar pruebas unitarias"
	@echo "  test-cov    Ejecutar pruebas con cobertura"
	@echo "  lint        Ejecutar linter (flake8)"
	@echo "  format      Formatear código (black)"
	@echo "  build       Construir imagen Docker"
	@echo "  run         Ejecutar contenedor Docker"
	@echo "  compose     Ejecutar con docker-compose"
	@echo "  clean       Limpiar archivos temporales"

install:
	@echo "Instalando dependencias..."
	pip install -r src/requirements.txt
	pre-commit install

test:
	@echo "Ejecutando pruebas..."
	cd src && pytest tests/ -v

test-cov:
	@echo "Ejecutando pruebas con cobertura..."
	cd src && pytest tests/ --cov=app --cov-report=html --cov-report=xml

lint:
	@echo "Ejecutando linter..."
	cd src && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	cd src && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "Formateando código..."
	cd src && black .

build:
	@echo "Construyendo imagen Docker..."
	docker build -t devops-microservice:latest .

run:
	@echo "Ejecutando contenedor..."
	docker run -p 5000:5000 --env-file .env devops-microservice:latest

compose:
	@echo "Ejecutando con docker-compose..."
	docker-compose up --build

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/ .pytest_cache/ .coverage