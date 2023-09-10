# Video Streaming Services API
This repository contains the implementation of API endpoints for user registration and payment processing for video streaming services.

## Prerequisites
- Python (v3.x recommended)
- Postman (for manual testing)

## Getting Started

### Setting up the virtual environment:
Before running the application, it's recommended to set up a virtual environment.

#### Install virtualenv:

```shell
pip install virtualenv
```

#### Create a virtual environment:
```shell
virtualenv venv
```

#### Activate the virtual environment:
On macOS and Linux:
```shell
source venv/bin/activate
```
On Windows:
```shell
.\venv\Scripts\activate
```

#### Installing required packages:
Once inside the virtual environment, navigate to the project root and install the required packages:

```shell
pip install -r requirements.txt
```

## Running the application:
Navigate to the root directory of the project and run:

```shell
python manage.py runserver
```

The server will start, and the API will be accessible at http://127.0.0.1:8000/.

# API Endpoints
### Registration:
- Endpoint: `/users`
- Method: POST
- Body: JSON with `'username'`, `'password'`, `'email'`, `'dob'`, and optionally `'credit_card_number'`.
### Get Registered Users:
- Endpoint: `/users`
- Method: GET
- Query Params: Optional `CreditCard` with values `'Yes'` or `'No'`.
### Payment:
- Endpoint: `/payments`
- Method: POST
- Body: JSON with `'credit_card_number'` and `'amount'`.


# Manual Testing with Postman
To manually test the API, it's recommended to use Postman.

1. Install and open Postman.
2. Use the provided API endpoints and their respective methods to test.
3. For POST requests, set the body type to JSON (application/json) and provide the required fields.
4. For GET requests on the /users endpoint, you can optionally provide query parameters.
5. Examine the HTTP status codes and response body for validation and confirmation of actions.

# Unit Testing
To run unit tests:

```shell
python manage.py test
```
