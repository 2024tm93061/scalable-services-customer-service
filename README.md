# Customer Service Microservice

The customers service is a microservice for managing customer profiles and KYC status using FastAPI and SQLAlchemy.

## Project Structure

```
customer-service
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── database.py      # Database connection logic
│   ├── models.py        # SQLAlchemy models for the Customer entity
│   └── crud.py          # CRUD operations for the Customer model
├── customers.csv        # Sample data for customers
├── Dockerfile            # Instructions to build the Docker image
├── docker-compose.yml    # Defines services for the Docker application
└── requirements.txt      # Python dependencies
```

## Quickstart (Docker)

1. Build the image and start the service:

```bash
docker-compose up --build
```

2. Open the API docs: http://localhost:8000/docs

The service uses a local SQLite file `customers.db` (mounted to the host). On first startup it will seed the DB from `customers.csv` if present.

3. Test Endpoints 

```python
python test_api.py
```

## Endpoints

- **Create Customer:** `POST /customers`
- **Read Customer:** `GET /customers/{customer_id}`
- **Update Customer:** `PUT /customers/{customer_id}`
- **Delete Customer:** `DELETE /customers/{customer_id}`
- **List Customers:** `GET /customers`

## Sample Data

The `customers.csv` file contains sample customer data that can be used for local development and testing.

## Requirements

Make sure to install the required dependencies listed in `requirements.txt` before running the application.

## Notes

This is a simple prototype and should be enhanced for production use, including error handling, logging, and security measures.