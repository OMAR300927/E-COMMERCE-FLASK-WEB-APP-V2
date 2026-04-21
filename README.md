# 🛒 E-Commerce Flask Web App - V2
A simple full-stack e-commerce system built for learning and production practice.

This is the second version of an e-commerce web application built with Flask.
In this version, the application has been deployed to the cluster using Kubernetes (minikube).
The application provides a complete shopping experience, including product management, user interactions, and online payments.

---

## 🚀 Features

### 👤 User Features

* Register and login
* Browse products
* Add products to shopping cart
* Update or remove cart items
* Checkout and purchase products using Stripe

### 🧑‍💼 Admin Features

* Secure admin panel
* Add new products
* Manage product listings

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS
* **Database:** PostgreSQL
* **Payments:** Stripe

---

⚙️ Setup
1. Clone the repository

git clone https://github.com/OMAR300927/E-COMMERCE-FLASK-WEB-APP-V2.git
cd E-COMMERCE-FLASK-WEB-APP-V2

2. Install dependencies

This project uses uv with pyproject.toml

uv sync

✔ This will automatically:

- Create a .venv virtual environment
- Install all required dependencies

3. Create .env file

FLASK_SQLALCHEMY_DATABASE_URI=your_postgres_url
FLASK_SECRET_KEY=your_secret_key
FLASK_JWT_SECRET_KEY=your_jwt_secret_key
FLASK_STRIPE_PUBLIC_KEY=your_stripe_public_key
FLASK_STRIPE_SECRET_KEY=your_stripe_secret_key
FLASK_CLIENT_ID=your_google_client_id
FLASK_CLIENT_SECRET=your_google_client_secret

4. Run the application

uv run run.py

---

## 📌 Notes

* Ensure PostgreSQL is running before starting the app
* Make sure the database is created (you can use tools like pgAdmin4)
* Stripe keys are required for payment functionality
* Admin routes are restricted to authorized users only
* Google credentials are required for authentication

---

## Improvements Added

* Added Redis for caching
* Added support for product images
* Added product search and filtering
* Dockerized the application using Docker
* Added Jenkins for CI/CD pipelines and SonarQube for code quality analysis
* Used Kubernetes to deploy the application

* For the secret file use the following command, you must replace localhost with `postgres-service`, which is defined in postgres.yaml in `FLASK_SQLALCHEMY_DATABASE_URI`.
```
kubectl create secret generic app-secrets \
  --from-literal=POSTGRES_DB=your_db_name \
  --from-literal=POSTGRES_USER=your_db_username \
  --from-literal=POSTGRES_PASSWORD=your_db_password \
  --from-literal=FLASK_SQLALCHEMY_DATABASE_URI=postgresql://your_db_username:your_db_password@postgres-service:5432/your_db_name \
  --from-literal=FLASK_SECRET_KEY=your_secret_key \
  --from-literal=FLASK_JWT_SECRET_KEY=your_jwt_secret_key \
  --from-literal=FLASK_CLIENT_ID=your_google_client_id \
  --from-literal=FLASK_CLIENT_SECRET=your_google_client_secret \
  --from-literal=FLASK_STRIPE_PUBLIC_KEY=your_stripe_public_key \
  --from-literal=FLASK_STRIPE_SECRET_KEY=your_stripe_secret_key
```

---

## 👨‍💻 Author

Omar Hussein
https://github.com/OMAR300927
