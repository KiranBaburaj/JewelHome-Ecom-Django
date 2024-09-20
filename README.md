# Jewel Home Project

**Jewel Home** is a full-stack e-commerce application designed to provide users with a seamless experience for browsing and purchasing jewelry online. The project is built using **Django** for the backend and **HTML/CSS** for the frontend, offering a user-friendly interface for both customers and administrators.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Recent Changes](#recent-changes)
- [Contributing](#contributing)


## Project Description

**Jewel Home** serves as an online platform for jewelry shopping, allowing users to:
- Browse a wide selection of jewelry items.
- View detailed product descriptions and images.
- Add items to their cart and proceed to checkout.
- Manage their user profiles and order history.

The admin panel enables the management of products, orders, and user accounts, providing a complete e-commerce solution. The application integrates **Google Authentication** for secure login and **Razorpay** for streamlined payment processing.

## Features

- **User Authentication**: Secure sign-up and login functionalities via Google Auth.
- **Product Catalog**: A comprehensive listing of jewelry products with filtering options.
- **Shopping Cart**: Add products to the cart, update quantities, and remove items.
- **Checkout Process**: Smooth checkout experience with Razorpay integration for payments.
- **User Profiles**: Users can manage their profiles and view order history.
- **Admin Dashboard**: Admin can add, update, and delete products and manage orders.

## Tech Stack

### Backend:
- **Django**: Web framework used for building the backend logic and managing database interactions.
- **PostgreSQL**: Relational database for storing product, user, and order information.

### Frontend:
- **HTML/CSS**: For creating the user interface and styling the application.

### Other Libraries:
- **Google Auth**: For user authentication.
- **Razorpay**: For payment processing.

## Setup and Installation

### Prerequisites:
- **Python 3.9+**
- **Django**
- **PostgreSQL**

### Clone the repository:

```bash
git clone https://github.com/KiranBaburaj/JewelHome-Ecom-Django.git
cd JewelHome-Ecom-Django




### Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the dependencies:

```bash
pip install -r requirements.txt
```

### Set up the database:

1. Create a PostgreSQL database for the project.
2. Update your database configuration in `settings.py`.
3. Run migrations to set up the database:

```bash
python manage.py migrate
```

4. Create a superuser for accessing the admin panel:

```bash
python manage.py createsuperuser
```

### Start the development server:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`.

## Usage

Once the server is running, users can:
- Sign up and log in to the application using Google Auth.
- Browse jewelry products and view details.
- Add items to their cart and complete purchases via Razorpay.
- Admin users can manage products and orders .


## Recent Changes

- Implemented user authentication via Google Auth.
- Integrated Razorpay for payment processing.
- Developed the product catalog with filtering options.
- Added shopping cart functionality and checkout process.
- Created an admin dashboard for product and order management.

## Contributing

Contributions are welcome! If you'd like to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

