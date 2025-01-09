# Development Guide for QR Code Generator

This document provides a guide for setting up and working on the QR Code Generator project. It covers the project structure, environment setup, running the application, and important development considerations.

## Table of Contents

1.  [Project Structure](#project-structure)
2.  [Prerequisites](#prerequisites)
3.  [Environment Setup](#environment-setup)
4.  [Running the Application](#running-the-application)
5.  [Docker Setup](#docker-setup)
6.  [Testing](#testing)
7.  [Important Considerations](#important-considerations)
8.  [Troubleshooting](#troubleshooting)

## 1. Project Structure

The project is organized into the following directories:

-   **`src`**: Contains all of the application's source code.
    -   **`app`**: Contains the application's modules and logic:
        -   `analytics`: Code related to analytics.
        -   `auth`: Code related to authentication.
        -   `qrcodes`: Code related to QR code generation.
    -   **`db`**: Code related to database interactions.
    -   `__init__.py`: Contains the Flask application setup.
    -   `config.py`: Contains the project configurations.
        **`test`**: Contains basic unit testings (auth routes only).
-   **`run.py`**: The entry point for starting the Flask application.
-   **`requirements.txt`**: Lists all Python dependencies.
-   **`Dockerfile`**: Defines the Docker image build process.
-   **`.dockerignore`**: Specifies files to ignore during Docker builds.
-   **`.env`**: Contains the project's environment variables (should not be committed).
-   **`Procfile`**: Contains instructions for deployment in platforms such as Heroku.
-   **`DEVELOPMENT.md`**: The file you are reading now.

## 2. Prerequisites

Before starting development, ensure you have the following installed:

-   **Python 3.11+**: The project uses Python 3.11.3 (or higher). You can download it from [python.org](https://www.python.org/).
-   **pip**: The Python package installer. It usually comes with Python.
-   **Docker Desktop**: For containerization. Download it from [docker.com](https://www.docker.com/).
-   **A Code Editor**: such as VS Code, PyCharm, or any other that you prefer.

## 3. Environment Setup

1.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    ```
2.  **Activate the Virtual Environment:**
    -   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    -   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` File:**

    -   Create a `.env` file in the project root directory and define environment variables needed for the project, for example:

        ```dotenv
        SECRET_KEY="your_secret_key"
        JWT_SECRET_KEY="your_jwt_secret_key"
        ACCESS_TOKEN_EXPIRES=3600
        REFRESH_TOKEN_EXPIRES=86400
        MONGODB_URI="mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=QRCode"
        DEBUG=True
        HOST="0.0.0.0"
        PORT=5000
        ```

        -   **Note:** Never commit your `.env` file to version control. Add `.env` to your `.gitignore`.

## 4. Running the Application

1.  **Start the Flask Development Server:**

    ```bash
    python run.py
    ```

    -   This command will start the Flask application on the specified host and port (you can check your config.py file for the configured values).

2.  **Access the application**:

-   Open a web browser and go to the specified host and port, usually `http://localhost:5000`.

## 5. Docker Setup

1.  **Build the Docker Image:**

    ```bash
    docker build -t qr-code-app .
    ```

    -   This command builds a Docker image using the instructions in your Dockerfile.

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
    -   This command runs the Docker container, mapping the port 5000 on your host to port 5000 inside the container.
    -   It also defines the necessary environment variables to the container.
3.  **Access the application:**

-   Open a web browser and go to `http://localhost:5000`

## 6. Testing

-   **Manual Testing:**
    -   Access all the functionalities in your frontend and make sure the requests and responses are working properly.
-   **Automated Tests:** To write automated tests, you can use the `pytest` library (or any other testing library), but this is beyond the scope of this document.

## 7. Important Considerations

-   **Environment Variables:** Always use environment variables for sensitive information. Never commit your `.env` file to version control. You can provide environment variables using the `-e` flag in the `docker run` command.
-   **`psycopg2`:** If you are using PostgreSQL, remember to use `psycopg2-binary` to avoid issues when building your Docker image.
-   **Frontend Configuration:** Make sure your frontend uses the correct backend API URL (usually `http://localhost:5000` when testing locally).
-   **Docker Secrets** For production deployment, consider using Docker secrets or a proper secrets management approach.
-   **Security**: Always take security into consideration, and handle your secrets properly.
-   **Dependencies**: Make sure to audit your `requirements.txt` and remove the packages that you are not using.
-   **Testing**: Use proper tests to ensure your app is working properly.
-   **Logging**: Create a proper loggin configuration for your app to debug any issues.

## 8. Troubleshooting

-   **Docker Issues:**
    -   If you encounter the `error during connect` when building, make sure Docker Desktop is running.
    -   If the build process fails due to `psycopg2` make sure you are using `psycopg2-binary` in your `requirements.txt`.
    -   If your container is failing, check your logs using the command `docker logs <container id>`
-   **Docker Networking:**
    -   If your frontend can't connect to the backend, make sure that you are using the right IP address (usually `localhost` for a local development setup).
    -   Check that the port mappings of your containers are working properly.
-   **Environment Variables:**
    -   If the application fails due to missing environment variables, provide them using the `-e` flag in `docker run`.

This guide should provide you with the necessary information to get started with development. If you encounter any issues or have further questions, feel free to consult the project's documentation or reach out for help.
