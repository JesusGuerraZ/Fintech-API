
## Requisitos

- Python 3.8 o superior
- PostgreSQL
- Redis
- Docker

## Uso


Para ejecutar todo el proyecto (API, base de datos, Redis y worker Celery) simplemente usa Docker Compose:

```
cd mi_api_rest
```

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

**Response:**
```json
{
  "id": 1,
  "owner_name": "Juan Pérez",
  "balance": 1000.0,
  "currency": "USD",
  "created_at": "2025-10-24T12:00:00Z",
  "updated_at": "2025-10-24T12:00:00Z"
}
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

**Response:**
```json
{
  "id": 1,
  "account": 1,
  "amount": 500.0,
  "type": "deposit",
  "description": "Depósito inicial",
  "created_at": "2025-10-24T12:01:00Z"
}
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

**Response:**
```json
{
  "id": 2,
  "account": 1,
  "amount": 200.0,
  "type": "withdrawal",
  "description": "Retiro de efectivo",
  "created_at": "2025-10-24T12:02:00Z"
}
```

## Logs de Transacciones

Cada vez que se crea una transacción, se registra un log tanto en la consola del worker Celery como en el archivo `logs/transactions.log`.
Este archivo se genera y actualiza dentro del contenedor Docker.

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

**Response:**
```json
{
  "id": 2,
  "owner_name": "Ana López",
  "balance": 500.0,
  "currency": "USD",
  "created_at": "2025-10-24T12:03:00Z",
  "updated_at": "2025-10-24T12:03:00Z"
}
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

**Response:**
```json
{
  "id": 3,
  "account": 1,
  "amount": 100.0,
  "type": "transfer",
  "destination_account": 2,
  "description": "Transferencia a Ana",
  "created_at": "2025-10-24T12:04:00Z"
}
```
### Ejemplo de error: saldo insuficiente

Si intentas realizar un retiro o transferencia y la cuenta no tiene suficiente saldo, la API responderá así:

#### Retiro con saldo insuficiente

```bash
curl -X POST http://localhost:8000/api/transactions/ \
		-H "Content-Type: application/json" \
		-d '{
				"account": 1,
				"amount": 99999,
				"type": "withdrawal",
				"description": "Intento de retiro sin fondos"
		}'
```

**Response:**
```json
{
	"detail": "Saldo insuficiente para el retiro."
}
```

#### Transferencia con saldo insuficiente

```bash
curl -X POST http://localhost:8000/api/transactions/ \
		-H "Content-Type: application/json" \
		-d '{
				"account": 1,
				"amount": 99999,
				"type": "transfer",
				"destination_account": 2,
				"description": "Intento de transferencia sin fondos"
		}'
```

**Response:**
```json
{
	"detail": "Saldo insuficiente para la transferencia."
}
```
