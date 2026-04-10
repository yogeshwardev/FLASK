# Flask MongoDB Atlas Demo

A complete full-stack Flask web application with:

- A Flask API route at `/api` that reads from `data.json`
- A Jinja2-based frontend form at `/`
- MongoDB Atlas integration using `pymongo`
- Success and error handling flows

## Project Structure

```text
project/
│── app.py
│── data.json
│── templates/
│   ├── form.html
│   └── success.html
│── requirements.txt
│── README.md
```

## Features

- Reads local JSON data and returns it using `jsonify()`
- Accepts `name` and `email` using an HTML form
- Inserts submitted data into MongoDB Atlas with `insert_one()`
- Redirects to `/success` after a successful insert
- Uses `try-except` blocks for clean error handling
- Shows inline error messages in the form template
- Includes required field validation and debug logs
- Runs directly with `python app.py`

## Installation

1. Create and activate a virtual environment.

   Windows PowerShell:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Set your MongoDB Atlas connection string as an environment variable.

   Windows PowerShell:

   ```powershell
   $env:MONGODB_URI="mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority&appName=Cluster0"
   ```

4. Run the application.

   ```powershell
   python app.py
   ```

5. Open the app in your browser.

   ```text
   http://127.0.0.1:5000/
   ```

## Routes

- `/` : Displays the form and handles form submission
- `/api` : Returns JSON data from `data.json`
- `/success` : Displays the success page

## MongoDB Notes

- Database: `testdb`
- Collection: `users`
- The app uses the `MONGODB_URI` environment variable by default
- If `MONGODB_URI` is not set, the app falls back to a placeholder URI in `app.py`

## Example API Response

```json
[
  {
    "id": 1,
    "name": "Alice"
  },
  {
    "id": 2,
    "name": "Bob"
  }
]
```

## Important

- Replace the placeholder MongoDB URI with your real MongoDB Atlas connection string
- Make sure your Atlas cluster allows your IP address
- Keep `debug=True` only for development
