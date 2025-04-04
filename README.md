
# AI Model Aggregator App

## Overview

Our project is an AI-powered application that gathers multiple AI models under one platform. The app allows users to select the best model that fits their use case from a variety of options, providing an intuitive and easy-to-use interface. Currently, the app integrates with APIs from OpenAI, Gemini, Hugging Face, and more to come in the future.

## Tech Stack

- **Frontend**: React with Vite
- **Backend**: Flask (Python)
- **Database**: MySQL
- **APIs**: OpenAI, Gemini, Hugging Face, and others (coming soon)

## Features

- Choose from a wide selection of AI models
- Streamlined interface to access different models for different tasks
- Integrates with multiple third-party AI APIs (e.g., OpenAI, Gemini)
- Simple, user-friendly experience for small businesses to access powerful AI tools


## Design System

### Color Palette
- **Primary**: Blues (#3498db, #71aeeb) - Foundation of the interface
- **Secondary**: Purple (#9b59b6) - Used for contrast and accent elements
- **Feedback**: Green (#2ecc71) for success, Red (#e74c3c) for alerts/errors
- **Text**: Dark (#2c3e50) to medium (#5a6577) hierarchy for readability

### Design Elements
- **Minimalist Approach**: Clean layouts with purposeful white space
- **Card-Based UI**: Information organized in consistent card components
- **Subtle Gradients**: Used for depth and visual interest
- **Typography**: Sans-serif system fonts optimized for legibility
- **Rounded Corners**: Consistent border-radius for a friendly feel

### Responsive Design
- Mobile-first approach with strategic element reorganization
- Touch-optimized controls on smaller screens
- Single-column layouts on mobile, multi-column on larger screens


## Database Structure

Our application uses a relational database with the following key tables:

### Tables & Relationships

**Users**
- Stores user credentials and profile information
- Has a one-to-one relationship with an active subscription

**Subscriptions**
- Records subscription details including purchase date
- Links to both users and subscription types
- Each subscription belongs to exactly one user

**Subscription Types**
- Defines available subscription plans and their pricing
- Multiple subscriptions can reference the same subscription type

This database design supports user management, subscription tracking, and subscription-based access control throughout the application.

## Installation

### Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (for frontend)
- [Python](https://www.python.org/) (for backend)
- [MySQL](https://www.mysql.com/) (for database)

### Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2.	Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate   
    ```

3.	Install the backend dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4.	Set up environment variables:
Create a .env file in the backend folder with the following content (adjust to your needs):
     ```sh

    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=password
    MYSQL_DB=yourdbname
    MYSQL_URL = "mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    OPENAI_API_KEY = ""
    GEMINI_API_KEY = ""
    HF_API_KEY = ""
    ```

5.	Run the Flask backend:
    ```sh
    flask run
    ```

### Frontend Setup

1.	Navigate to the frontend folder:
    ```sh
    cd frontend
    ```


    ```sh
    npm install
    ```


    ```sh
    npm run dev
    ```

## Cypress Testing for IN1 Frontend

This directory contains end-to-end tests using Cypress.

### Test Structure

- **Login & Authentication**: login.cy.js
- **Subscription Management**: subscription.cy.js
- (Other test categories)

### Running Tests

- Local development: `npm run cypress:open`
- Headless mode: `npm run cypress:run`
- CI/CD: Automatically runs on push to main/develop

### Mock Strategy

Tests use API mocking to isolate frontend testing from backend dependencies


## Version Control

We use Git for version control. Ensure that your changes are committed to the repository.

### Git Commit structure
```sh
<type>(<scope>): <short summary>
<references>
```

### Exmaple:
```sh
feat(auth): add login API
Closes #123
Fixes #456
```

### Type
The type describes the kind of change that the commit introduces.
The most common types are:

    feat: A new feature for the user.
    fix: A bug fix.
    docs: Documentation changes.
    style: Code style changes (formatting, white space, etc.) that do not affect the logic.
    refactor: A code change that neither fixes a bug nor adds a feature, but improves the structure or clarity of the code.
    test: Adding or modifying tests.
    merge conflicts: Resolved between dev and feature-xyz

### Scope (optional)
The scope is optional but can be added to describe the area of the project that the commit is related to:

    e.g.
    a particular module
    a component
    a functionality


## Contributing
1.	Fork the repository.
2.	Create your feature branch: git checkout -b feature-name.
3.	Commit your changes: git commit -m 'Add new feature'.
4.	Push to the branch: git push origin feature-name.
5.	Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
•	OpenAI
•	Gemini
•	Hugging Face