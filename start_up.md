# 🚀 Full-Stack Development Setup (React + Flask + MySQL)

## 📌 Prerequisites
- Install [Node.js](https://nodejs.org/) & [npm](https://www.npmjs.com/)
- Install [Python](https://www.python.org/) & [pip](https://pypi.org/project/pip/)
- Install MySQL and set up a database
- Install [Git](https://git-scm.com/)

---

## 🏗️ Backend Setup (Flask + MySQL)

### 1️⃣ **Create a Virtual Environment**
```sh
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2️⃣ **Install Flask & Dependencies**
```sh
pip install -r requirements.txt
# flask flask-cors flask-sqlalchemy mysql-connector-python gunicorn
```
<!-- What is mysql-connector and gunicorn -->

### 3️⃣ **Initialize Flask App (`app.py`)**
```python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return jsonify({"message": "Hello, Flask!"})

if __name__ == "__main__":
    app.run(debug=True)
```

### 4️⃣ **Run Flask App**
```sh
flask run
```

---

## 🎨 Frontend Setup (React + Vite)

### 1️⃣ **Create React App with Vite**
```sh
# Install Vite and create a React project
npm create vite@latest frontend --template react
cd frontend
npm install
```

### 2️⃣ **Install Required Dependencies**
```sh
npm install axios react-router-dom
```

### 3️⃣ **Run React App**
```sh
npm run dev
```

---

## 🔍 API Calls (Axios)
### 1️⃣ **Install Axios**
```sh
npm install axios
```
### 2️⃣ **Create API Call (`api.js`)**
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const fetchData = async () => {
    try {
        const response = await axios.get(`${API_URL}/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching data", error);
    }
};
```

---

## ✅ Code Quality & Formatting

### 1️⃣ **Backend (Python Linters & Formatters)**
```sh
pip install black flake8 isort
```

#### **Run Formatters**
```sh
black .
isort .
flake8 .
```

### 2️⃣ **Frontend (ESLint & Prettier)**
```sh
npm install --save-dev eslint prettier eslint-config-prettier eslint-plugin-prettier
```

#### **Create `.eslintrc.json`**
```json
{
  "extends": ["eslint:recommended", "plugin:react/recommended", "prettier"],
  "rules": {
    "prettier/prettier": ["error"]
  }
}
```

#### **Run Formatters**
```sh
npx prettier --write .
npx eslint . --fix
```

---

## 🧪 Testing Setup

### 1️⃣ **Backend Testing with Pytest**
```sh
pip install pytest
pytest
```

### 2️⃣ **Frontend Testing (React Testing Library)**
```sh
npm install --save-dev @testing-library/react @testing-library/jest-dom
```
```sh
npm test
```

---

## 🎯 Version Control (Git)
```sh
git init
echo "venv/" >> .gitignore
echo "node_modules/" >> .gitignore
git add .
git commit -m "Initial commit"
```

---

## 🔥 Additional Considerations
- **Use `.env` files** for sensitive information
- **Dockerize the application** for easier deployment
- **Setup CI/CD (GitHub Actions, Docker, etc.)**
- **Use Swagger (`flasgger`) for API documentation**

🚀 **You're all set! Happy Coding!** 🎉
