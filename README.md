# QR Code Generator

Backend for QR Code - Junction CTO assignment
A web application for generating, managing, and deleting QR codes.

## Overview

The QR Code Generator is a web application designed to provide users with an easy and convenient way to create and manage QR codes. Users can generate QR codes for URLs and customize them with a title, foreground color, background color, and a logo. The application provides secure user authentication and allows users to view and manage their generated QR codes.

## Features

-   **User Authentication:** Secure user registration and login.
-   **QR Code Generation:** Generates customizable QR codes for URLs.
-   **Customization:** Allows users to set a title, foreground color, background color and upload a logo.
-   **QR Code Management:** Users can view, download, and delete their generated QR codes.
-   **REST API:** Provides a RESTful API for interacting with the application.

## Technologies Used

-   **Backend:**
    -   Python 3.11+
    -   Flask (Web Framework)
    -   PyJWT (JSON Web Tokens)
    -   bcrypt (Password Hashing)
    -   pymongo (MongoDB Driver)
    -   qrcode (QR Code Generation)
    -   gunicorn (WSGI server)
    -   `pillow` (Image manipulation)
-   **Containerization:**
    -   Docker
-   **Dependencies:**
    -   Listed in the requirements.txt
-   **Frontend:** _(you can add this if you are using a specific frontend framework/library)_
    -   You should add it if you have any

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

-   Python 3.11+ ([python.org](https://www.python.org/))
-   pip (Python package installer)
-   Docker Desktop ([docker.com](https://www.docker.com/))

### Local Development Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    ```
3.  **Activate the Virtual Environment:**
    -   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    -   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Create a `.env` File:**

    -   Create a `.env` file and populate it with your environment variables.

6.  **Run the Application:**
    ```bash
    python run.py
    ```
7.  **Access the Application**
    -   Open a web browser and go to `http://localhost:5000`.

### Docker Setup

1.  **Build the Docker Image:**
    ```bash
    docker build -t qr-code-app .
    ```
2.  **Run the Docker Container:**

    ```bash
    docker run -p 5000:5000 \
          -e SECRET_KEY="your_secret_key" \
          -e JWT_SECRET_KEY="your_jwt_secret_key" \
          -e ACCESS_TOKEN_EXPIRES=3600 \
          -e REFRESH_TOKEN_EXPIRES=86400 \
          -e MONGODB_URI="your_mongodb_uri" \
          -e DEBUG="True" \
          -e HOST="0.0.0.0" \
          -e PORT=5000 \
          qr-code-app
    ```

3.  **Access the Application**
    -   Open a web browser and go to `http://localhost:5000`.

## API Documentation

-   For detailed information about the API endpoints, please refer to the [DOCUMENTATION.md](DOCUMENTATION.md) file.

## Development Guide

-   For detailed information about setting up your development environment, check the [DEVELOPMENT.md](DEVELOPMENT.md) file.

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the [Your License] - see the LICENSE.md file for details. _If you want to add a license_
