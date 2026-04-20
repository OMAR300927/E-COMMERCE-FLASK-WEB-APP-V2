# 🛒 E-Commerce Flask Web App- V2
A simple full-stack e-commerce system built for learning and production practice.

Socend version of an e-commerce web application built with Flask.
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

git clone https://github.com/OMAR300927/E-COMMERCE-FLASK-WEB-APP-V1.git
cd E-COMMERCE-FLASK-WEB-APP-V1

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

4. Run the application

uv run run.py

---

## 📌 Notes

* Ensure PostgreSQL is running before starting the app
* Make sure the database is created (you can use tools like pgAdmin4)
* Stripe keys are required for payment functionality
* Admin routes are restricted to authorized users only

---

## The future has been added 

* Add Redis for caching 
* Add Google authentication 
* Support product images 
* Add product search and filtering 
* Dockerize the application using docker
* Use Jenkins for CI/CD pipelines and SonarQube for code quality analysis

---

## 👨‍💻 Author

Omar Hussein
https://github.com/OMAR300927
