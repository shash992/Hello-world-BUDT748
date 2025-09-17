# User Management System - BUDT748

**Author:** Sai Shashank Kudkuli (Section 501)

## Project Description

A full-stack web application for managing users built with Flask and MySQL. This project demonstrates CRUD (Create, Read, Update, Delete) operations through a clean web interface.

## Features

- **Add Users**: Create new users with name and email
- **View Users**: Display all users in a dynamic table
- **Delete Users**: Remove users from the database
- **Real-time Updates**: Interface updates automatically after operations
- **Responsive Design**: Bootstrap-powered UI that works on all devices

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL with Flask-MySQLdb
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (jQuery)
- **Environment**: UV package manager with virtual environment
- **Security**: Environment variables for database credentials

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Set up MySQL Database**:
   - Create a database named `user_management`
   - Create a `users` table with columns: `id`, `name`, `email`

3. **Configure Environment Variables**:
   - Create a `.env` file in the project root
   - Add your MySQL password: `MYSQL_PASSWORD=your_password`

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   - Open your browser to `http://127.0.0.1:5000`

## API Endpoints

- `GET /` - Home page with user interface
- `POST /user` - Add a new user (JSON)
- `GET /users` - Retrieve all users (JSON)
- `DELETE /user/<id>` - Delete a user by ID

## Project Structure

```
hello-world/
├── app.py              # Main Flask application
├── templates/
│   └── home.html       # Frontend interface
├── .env               # Environment variables (not in git)
├── pyproject.toml     # Project dependencies
└── README.md          # This file
```
