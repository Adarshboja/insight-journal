# insight-journal: Developer Journal API

## Overview

`insight-journal` is an API-first Python project designed for developers to record and manage structured engineering notes. It provides a robust backend for capturing insights, solutions, debugging steps, and general technical thoughts in a searchable and organized manner, promoting knowledge retention and efficient project management.

**Key Features:**
*   **Structured Entries:** Define custom fields for consistent note-taking.
*   **Search & Filter:** Easily retrieve notes based on keywords, tags, or date ranges.
*   **RESTful API:** Programmatic access for integration with custom tools or frontends.
*   **Developer-Focused:** Optimized for tracking technical information, code snippets, and issue resolutions.

## Setup

This guide assumes you have Python 3.8+ and `git` installed.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/insight-journal.git
    cd insight-journal
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root based on `config.example.env`.
    ```dotenv
    # config.example.env (copy this to .env and fill in)
    SECRET_KEY="your_super_secret_key_here"
    DATABASE_URL="sqlite:///./insight_journal.db" # Or your PostgreSQL/MySQL URL
    API_AUTH_TOKEN="your_secure_api_token" # For simple API key auth
    DEBUG=True # Set to False for production
    ```
    *   **`SECRET_KEY`**: A strong, random string for security.
    *   **`DATABASE_URL`**: Connection string for your database.
    *   **`API_AUTH_TOKEN`**: A token for API authentication (for production, consider a more robust auth solution).

5.  **Initialize Database:**
    Apply any database migrations. (Assuming SQLAlchemy/Alembic or similar)
    ```bash
    flask db upgrade # Or similar command based on your ORM/framework
    ```

6.  **Run the Development Server:**
    ```bash
    flask run
    ```
    The API will typically be available at `http://127.0.0.1:5000`.

    **For Production:** Use a WSGI server like Gunicorn:
    ```bash
    gunicorn -w 4 "app:create_app()" # Replace 'app:create_app()' with your actual WSGI entry point
    ```

## Usage

Interact with the API using standard HTTP methods. All requests require an `X-API-KEY` header for authentication, using the `API_AUTH_TOKEN` defined in your `.env`.

**Base URL:** `http://127.0.0.1:5000/api/v1` (adjust if running on a different port/domain)

---

### **1. Create a New Entry (POST /entries)**

Create a new structured note.

**Request:**
```bash
curl -X POST \
  -H "X-API-KEY: your_secure_api_token" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Debugging a race condition in payment service",
        "content": "Identified a potential race condition when processing concurrent payment requests due to shared mutable state. Implemented a mutex lock around the critical section.",
        "tags": ["bug", "concurrency", "payment-service"],
        "project": "E-commerce Platform",
        "priority": "High"
      }' \
  http://127.0.0.1:5000/api/v1/entries
```

**Response (201 Created):**
```json
{
  "id": "abc-123",
  "title": "Debugging a race condition...",
  "content": "Identified a potential race condition...",
  "tags": ["bug", "concurrency", "payment-service"],
  "project": "E-commerce Platform",
  "priority": "High",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

---

### **2. Retrieve All Entries (GET /entries)**

Get a list of all journal entries.

**Request:**
```bash
curl -X GET \
  -H "X-API-KEY: your_secure_api_token" \
  http://127.0.0.1:5000/api/v1/entries
```

**Response (200 OK):**
```json
[
  {
    "id": "abc-123",
    "title": "Debugging a race condition...",
    "tags": ["bug", "concurrency"],
    "created_at": "2023-10-27T10:00:00Z"
  },
  {
    "id": "def-456",
    "title": "Optimizing database queries for dashboard",
    "tags": ["performance", "database"],
    "created_at": "2023-10-26T14:30:00Z"
  }
]
```

---

### **3. Search Entries (GET /entries?q=...)**

Search for entries by keyword in title or content.

**Request:**
```bash
curl -X GET \
  -H "X-API-KEY: your_secure_api_token" \
  "http://127.0.0.1:5000/api/v1/entries?q=race%20condition&tag=bug"
```

**Response (200 OK):**
```json
[
  {
    "id": "abc-123",
    "title": "Debugging a race condition...",
    "tags": ["bug", "concurrency"],
    "created_at": "2023-10-27T10:00:00Z"
  }
]
```