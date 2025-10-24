## Requisitos

- Python 3.8 o superior
- PostgreSQL
- Redis
- Docker

## Uso

Para ejecutar todo el proyecto (API, base de datos, Redis y worker Celery) simplemente usa Docker Compose:

```
docker-compose up --build
```

Esto levantará automáticamente:
- La API en `http://localhost:8000/`
- PostgreSQL como base de datos
- Redis como broker de mensajes
- El worker de Celery para tareas asíncronas

No necesitas ejecutar comandos adicionales para Celery, ya que el worker se inicia automáticamente con Docker Compose.

## Endpoints

- **Cuentas**: `/api/accounts/`
- **Transacciones**: `/api/transactions/`
- **Swagger**: `/api/swagger/` 


## Ejemplos de Uso de la API

A continuación se muestra cómo interactuar con la API paso a paso usando `curl`:

### 1. Crear una cuenta

```bash
curl -X POST http://localhost:8000/api/accounts/ \
	-H "Content-Type: application/json" \
	-d '{
		"owner_name": "Juan Pérez",
		"balance": 1000,
		"currency": "USD"
	}'
```

### 2. Realizar un depósito

```bash
curl -X POST http://localhost:8000/api/transactions/ \
	-H "Content-Type: application/json" \
	-d '{
		"account": 1,
		"amount": 500,
		"type": "deposit",
		"description": "Depósito inicial"
	}'
```

### 3. Realizar un retiro

```bash
curl -X POST http://localhost:8000/api/transactions/ \
	-H "Content-Type: application/json" \
	-d '{
		"account": 1,
		"amount": 200,
		"type": "withdrawal",
		"description": "Retiro de efectivo"
	}'
```

## Logs de Transacciones

Cada vez que se crea una transacción, se registra un log tanto en la consola del worker Celery como en el archivo `logs/transactions.log`.
Este archivo se genera y actualiza dentro del contenedor Docker, pero si el volumen de la carpeta `logs` está correctamente montado en Docker Compose, podrás ver los cambios reflejados también en tu máquina local y en Visual Studio Code.
### 4. Realizar una transferencia

Primero crea una segunda cuenta:

```bash
curl -X POST http://localhost:8000/api/accounts/ \
	-H "Content-Type: application/json" \
	-d '{
		"owner_name": "Ana López",
		"balance": 500,
		"currency": "USD"
	}'
```

Luego realiza la transferencia de la cuenta 1 a la cuenta 2:

```bash
curl -X POST http://localhost:8000/api/transactions/ \
	-H "Content-Type: application/json" \
	-d '{
		"account": 1,
		"amount": 100,
		"type": "transfer",
		"destination_account": 2,
		"description": "Transferencia a Ana"
	}'
```