# UltrokPay - The Universal Marketplace

Welcome to UltrokPay, an enterprise-grade universal marketplace and payment system developed by Ultrok Enterprise. This platform allows users to buy and sell a wide variety of digital and physical products, with transactions powered by the Pi and Sidra cryptocurrencies.

## Features

- **Modular Architecture**: Built with Django, the project is structured into modular apps for maintainability and scalability.
- **Dual Currency Support**: Natively supports both Pi and Sidra currencies, with real-time price conversions displayed in USD.
- **Blockchain Escrow**: Transactions are secured by the `UltrokPayEscrow` Solidity smart contract, ensuring safety for both buyers and sellers.
- **Digital & Physical Products**: Supports a wide range of products, from ebooks and software to electronics and clothing.
- **Real-time Chat**: Buyers and sellers can communicate in real-time on order pages via Django Channels.
- **RESTful API**: A comprehensive API built with Django Rest Framework provides endpoints for all major functionalities, with JWT authentication.
- **Background Tasks**: Celery and Redis handle asynchronous tasks like blockchain polling and notifications.
- **Containerized & Deployable**: Comes with Docker and Render configurations for easy setup and deployment.

## Getting Started

Follow these instructions to get the UltrokPay platform running on your local machine for development and testing purposes.

### 1. Environment Setup

The project uses environment variables for configuration. Start by creating a `.env` file in the project root by copying the example file:

```bash
cp .env.example .env
```

Now, open the `.env` file and customize the variables as needed. At a minimum, you should set a new `SECRET_KEY`. For local development, the default database and Redis URLs will work if you are using the provided `docker-compose.yml`.

### 2. Installing Dependencies

All Python dependencies are listed in `requirements.txt`. While Docker handles this for you, you can set up a local virtual environment and install them with:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Running with Docker (Recommended)

The easiest way to get all services running is with Docker Compose.

**Start all services:**
```bash
docker-compose up --build
```
This will build the Docker images and start containers for the web server, PostgreSQL database, Redis, Celery worker, and Celery Beat scheduler. The web application will be available at `http://localhost:8000`.

### 4. Database Migrations

Once the `db` service is running, you need to apply the database migrations. Open a new terminal and run:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a Superuser

To access the Django admin interface, create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### 6. Load Sample Data

To populate the database with sample users, categories, and products, run the `seed_data` management command:

```bash
docker-compose exec web python manage.py seed_data
```
This will create:
- An admin user (`admin@ultrokpay.com`, password: `adminpassword`)
- A sample buyer (`buyer1@example.com`, password: `password123`)
- Two sample sellers (`seller1@example.com`, `seller2@example.com`)
- Sample product categories and products.

### 7. Running Tests

The project includes a test suite built with `pytest`. To run the tests, execute the following command:

```bash
docker-compose exec web pytest
```
*Note: The test environment in some remote execution contexts may have issues discovering installed packages. The Docker environment is the most reliable way to run the test suite.*

## Pricing Logic

- **Sidra (SDR)**: The value of Sidra is intended to be stable and is configured via the `SIDRA_NGN_RATE` environment variable. The default is **50 Nigerian Naira (NGN)** per Sidra coin. The `NGN_USD_RATE` is used for conversion to USD.
- **Pi (PI)**: The value of Pi is volatile. The `PI_USD_RATE` environment variable provides a fallback value. In a production environment, this rate should be updated periodically by a background task fetching data from an external pricing API.
- **User Interface**: All prices are displayed to the user in **USD**, with the equivalent cost in Pi and Sidra shown for clarity at checkout and on product pages.

## Deployment to Render

This project is configured for easy deployment to [Render](https://render.com/). The `render.yaml` file in the root directory defines all the necessary services.

To deploy:
1. Create a new "Blueprint" on Render.
2. Connect the Git repository for this project.
3. Render will automatically detect and use the `render.yaml` file to provision the database, Redis instance, web server, and background workers.

Environment variables defined in your Blueprint will override any defaults. Ensure you set a secure `SECRET_KEY` and other production-level configurations in the Render dashboard.
