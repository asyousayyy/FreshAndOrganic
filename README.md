# Fresh&Organic E-Commerce Website Project

Welcome to the **Fresh&Organic E-Commerce Website Project**! This project demonstrates a fully functional online store where users can browse products, manage their shopping cart, and access personalized profiles. The platform integrates payment gateways and offers robust features for users and sellers.

## Live Demo

Explore the live application here: [Fresh&Organic Live](https://freshandorganic.pythonanywhere.com)

## GitHub Repository

The source code for this project is available at: [Fresh&Organic GitHub](https://github.com/ankitismyname/Fresh-Organic)

## Features

- **Shopping Cart System**: Users can add items to their cart, view the cart, and proceed to checkout. Cart quantities are limited per product to ensure proper inventory management.
- **Login/Logout System**: Secure user authentication with PBKDF2_SHA256 encryption and CSRF protection.
- **User Profile Pages**: Users can edit their details, change passwords, and view order history, with a simple interface for personal management.
- **Seller Functionality**: Verified users can become sellers, with access to product management through CRUD operations.
- **Payment Gateway**: Integrated with **Stripe** for secure online payments. Also supports **Cash on Delivery (COD)**, with additional charges applied to COD orders.
- **Contact Support**: An email-based system where users can report issues or request assistance.

## Technologies Used

- **HTML**: Structures and presents the content of web pages.
- **CSS & Bootstrap**: Used for styling and ensuring responsive layouts with pre-built components.
- **DOM API**: Facilitates dynamic updates to the page content.
- **Django**: Backend framework to handle server-side logic, manage the database, and implement security measures like CSRF protection.
- **PBKDF2_SHA256**: Used for secure password encryption.
- **Stripe**: Provides seamless integration for processing online payments.

## Tools Used

- **Visual Studio Code**: The integrated development environment used for development.
- **Web Browser**: Used to test and interact with the website during development.

## Getting Started

To run the project locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/ankitismyname/Fresh-Organic.git
    cd Fresh-Organic
    ```

2. **Set up a virtual environment** (recommended):

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

5. **Open your web browser** and visit `http://localhost:8000` to explore the website.

## Contributing

We welcome contributions to this project! Here's how you can get involved:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the changes to your branch (`git push origin feature/YourFeature`).
5. Open a Pull Request for review.

---

## Acknowledgments

- Many thanks to the **Django** and **Bootstrap** communities for their extensive resources and support.

