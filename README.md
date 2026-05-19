# URL Shortener — FastAPI + PostgreSQL

A production-style URL shortener built with FastAPI, SQLAlchemy, and PostgreSQL.

## Project Structure

```
url-shortener/
├── app/
│   ├── main.py        # FastAPI app + all routes
│   ├── database.py    # DB connection & session setup
│   ├── models.py      # SQLAlchemy table definitions
│   ├── schemas.py     # Pydantic request/response shapes
│   ├── crud.py        # Database operations
│   └── utils.py       # Short code generator
├── static/
│   └── index.html     # Frontend UI
├── .env               # Your credentials (never commit this)
├── requirements.txt
└── README.md
```

## Setup

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
Make sure PostgreSQL is running, then create the database:
```bash
psql -U postgres
CREATE DATABASE urlshortener;
\q
```

### 4. Configure your .env file
Edit `.env` and update your PostgreSQL password:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/urlshortener
BASE_URL=http://localhost:8000
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

The `--reload` flag restarts the server automatically when you change a file.

## Usage

- **Frontend UI**: http://localhost:8000/static/index.html
- **API Docs** (auto-generated): http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/{short_code}` | Redirect to the original URL |
| GET | `/health` | Health check |

### Example: Shorten a URL
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://www.example.com/very/long/path"}'
```

Response:
```json
{
  "short_code": "aB3xP7",
  "long_url": "https://www.example.com/very/long/path",
  "short_url": "http://localhost:8000/aB3xP7",
  "created_at": "2024-01-15T10:30:00Z"
}
```
