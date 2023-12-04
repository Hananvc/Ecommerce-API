#E-commerce API
Welcome to the Django E-Commerce API project! This API is built using Django Rest Framework to manage customers, orders, and products in an e-commerce system.

## Features

- Manage customers, orders, and products.
- List, create, and update customers.
- List, create, and update products.
- List, create, and update orders.
- Search for orders based on products or customers.


## Getting Started

### Prerequisites

Before you start, make sure you have the following installed:

- Python (>=3.6)
- Django
- Django Rest Framework

### Installation

1. Clone the repository:
     git clone https://github.com/Hananvc/Ecommerce-API.git
2. Navigate to the project directory:
     cd Ecommerce
3. Install dependencies:
     pip install -r requirements.txt
4. Apply database migrations:
     python manage.py migrate
5. Run the development server:
     python manage.py runserver

Now, your Django E-Commerce API should be up and running.

###Usage
API Endpoints
  Customers:
    List all customers: GET /api/customers/
    Create a new customer: POST /api/customers/
    Update existing customer: PUT /api/customers/<id>/
Products:
    List all products: GET /api/products/
    Create a new product: POST /api/products/
Orders:
    List all orders: GET /api/orders/
    Create a new order: POST /api/orders/
    Edit existing order: PUT /api/orders/<id>/
    List order based on products: GET /api/orders/?products=Product1,Product2
    List order based on customer: GET /api/orders/?customer=JohnDoe
  
Validations to keep in mind:
  Customer's and product’s name must be unique.
  Weight in positive decimal and not more than 25kg.
  Order cumulative weight must be under 150kg.
  Order Date cannot be in the past.

