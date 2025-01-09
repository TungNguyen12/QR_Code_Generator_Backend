# QR Code Generator - User Documentation

This document provides instructions on how to use the QR Code Generator application. It covers the main features, how to access them, and any important considerations for end-users.

## Table of Contents

1.  [Introduction](#introduction)
2.  [Accessing the Application](#accessing-the-application)
3.  [User Registration](#user-registration)
4.  [User Login](#user-login)
5.  [Generating QR Codes](#generating-qr-codes)
6.  [Viewing My QR Codes](#viewing-my-qr-codes)
7.  [Deleting QR Codes](#deleting-qr-codes)
8.  [API Documentation](#api-documentation)

## 1. Introduction

The QR Code Generator is a web application that allows users to create, manage, and delete QR codes. Users can generate QR codes for URLs and optionally customize them with a title, foreground color, background color, and a logo.

## 2. Accessing the Application

To access the application:

1.  Open your web browser.
2.  Navigate to the URL where the application is hosted. This could be `http://localhost:5000` if you're running it locally, or a specific domain name if deployed on a server.

## 3. User Registration

New users need to register before using the application:

1.  Navigate to the registration page. This is typically accessed by clicking a "Register" link or button on the login page.
2.  Fill in the required fields:
    -   Username
    -   Email Address
    -   Password
3.  Click the "Register" button.
4.  If registration is successful, you will receive a success message and be redirected to the login page.

## 4. User Login

Existing users can log in:

1.  Navigate to the login page.
2.  Enter your registered email address and password.
3.  Click the "Login" button.
4.  Upon successful login, you'll be redirected to the main application dashboard.

## 5. Generating QR Codes

Once logged in, you can generate QR codes:

1.  Navigate to the "Generate QR Code" page.
2.  Fill in the required fields:
    -   **URL:** The URL that the QR code should point to.
    -   **Title:** (Optional) A title for your QR code.
    -   **Foreground Color:** (Optional) The foreground color of the QR code (e.g., `#000000` for black).
    -   **Background Color:** (Optional) The background color of the QR code (e.g., `#ffffff` for white).
    -   **Logo:** (Optional) A logo image that will be displayed in the center of the QR code.
3.  Click the "Generate" button.
4.  The generated QR code image will be displayed and will be available for download.

## 6. Viewing My QR Codes

To view the QR codes you have generated:

1.  Navigate to the "My QR Codes" page.
2.  A list of all your QR codes will be displayed.
3.  Each QR code will have a title and will be available for download.

## 7. Deleting QR Codes

To delete your QR Codes:

1. Navigate to the "My QR Codes" page.
2. Locate the specific QR code you want to delete from the list.
3. Click the "Delete" button next to the selected QR code.
4. A confirmation message will be displayed, indicating that the QR code has been successfully deleted.

## 8. API Documentation

The backend API provides the following endpoints:

-   **`POST /auth/register`:** Registers a new user.
    -   **Request Body:**
        ```json
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
        ```
    -   **Response:**
        -   Success (201):


            ```json
            {
              "message": "User registered successfully",
              "user_id": "string"
            }
            ```
        -   Error (400):


            ```json
            {
               "error": "All fields are required"
            }
            ```
        -   Error (400):


            ```json
            {
              "error": "User already exists"
            }
            ```
-   **`POST /auth/login`:** Logs in an existing user.
    -   **Request Body:**
        ```json
        {
            "email": "string",
            "password": "string"
        }
        ```
    -   **Response:**
        -   Success (200):
            ```json
            {
                "message": "Login successful",
                "access_token": "string",
                "refresh_token": "string"
            }
            ```
        -   Error (400):
            ```json
            {
                "error": "Email and password are required"
            }
            ```
        -   Error (401):
            ```json
            {
                "error": "Invalid email or password"
            }
            ```
-   **`POST /auth/refresh`:** Refreshes an expired access token using a refresh token.
    -   **Request Body:**


        ```json
        {
          "refresh_token": "string"
        }
        ```
    -   **Response:**
    -   Success (200):
        ```json
        {
            "access_token": "string"
        }
        ```
    -   Error (401):
        ```json
        {
            "error": "Invalid or expired refresh token"
        }
        ```
    -   Error (400):
        ```json
        {
            "error": "Invalid request data"
        }
        ```
    -   Error (400):
        ```json
        {
            "error": "Invalid refresh token format"
        }
        ```
-   **`POST /qrcodes/generate`:** Generates a QR code.
    -   Requires a valid `Authorization` header containing a JWT token.
    -   **Request Body:**
        ```json
        {
            "url": "string",
            "title": "string",
            "foreground_color": "string",
            "background_color": "string"
        }
        ```
    -   **Response**:
        -   Success (200): Returns a `png` image of the generated QR code.
        -   Error (401):


            ```json
             {
                "error": "Unauthorized"
             }
            ```
        -   Error (400):
            ```json
            {
                "error": "No URL provided"
            }
            ```
-   **`GET /qrcodes/my_qrcodes`:** Retrieves all QR codes of a specific user.
    -   Requires a valid `Authorization` header containing a JWT token.
    -   **Response:**
        -   Success (200):
            ```json
            [
                {
                    "_id": "string",
                    "user_id": "string",
                    "url": "string",
                    "title": "string",
                    "foreground_color": "string",
                    "background_color": "string",
                    "logo_path": "string",
                    "created_at": "date_string"
                }
            ]
            ```
    -   Error (401):
        ```json
        {
            "error": "Unauthorized"
        }
        ```
-   **`DELETE /qrcodes/qrcodes/<qr_code_id>`:** Deletes a QR code by ID.
    -   Requires a valid `Authorization` header containing a JWT token.
    -   **Response**:
        -   Success (200):
            ```json
            {
                "message": "QR code deleted successfully"
            }
            ```
        -   Error (401):
            ```json
            {
                "error": "Unauthorized"
            }
            ```
        -   Error (404):
            ````json
               {
                  "error": "QR code not found or unauthorized"
                }
               ```
            ````

This documentation is intended to help users effectively utilize the QR Code Generator. If you encounter any issues, please consult the project maintainers or provide feedback.
