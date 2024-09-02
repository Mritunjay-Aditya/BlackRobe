# BlackRobe

**BlackRobe** is a judiciary application designed to streamline court case management and administrative tasks. Built with Flask and MongoDB, it offers a secure platform for managing legal proceedings, user authentication, and document handling. The application includes features such as user registration, secure login, case tracking all within a user-friendly interface. BlackRobe adheres to best practices in data security, making it an ideal solution for law firms, courts, and legal professionals. It ensures that justice is managed efficiently and transparently.

## Features

- **User Registration and Authentication**
  - Email verification and encrypted passwords
  - Password reset via email
  - Role-based access control with admin validation

- **Case Management**
  - Manage legal cases and track court proceedings
  - Assign cases to judges and attorneys

- **Admin Dashboard**
  - User and case management with role permissions
  - Validation of new users

- **Security**
  - Token-based authentication and session management
  - Secure data storage with MongoDB Atlas

## Installation

### Prerequisites
- Python 3.8+
- Django 3.x+
- MongoDB Atlas account





### Getting Started
### Prerequisites

- Python 3.x
- Flask

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. Set the Flask app environment variable:
    ```sh
    set FLASK_APP=app.py
    ```

2. Run the Flask application:
    ```sh
    flask run
    ```

3. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Project Details

### File Structure

- `templates/`: Contains HTML templates.
- `assets/`: Contains static files like images, CSS, and JavaScript.
- `instance/`: Contains instance-specific files (e.g., configuration, database).
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `app.py`: The main Flask application file.

### .gitignore
The`.gitignore` file includes the following:

```ignore
### Flask ###
instance/*
!instance/.gitignore
.webassets-cache
.env
```










## Acknowledgments

Made with 💻 and ☕ by [Your Name](https://github.com/Mritunjay-Aditya).
