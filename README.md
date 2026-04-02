# Candidate Management API

REST API backend for managing recruitment candidates. Built with FastAPI, MongoDB natively using Motor, and Pydantic V2.

### Live Deployment
[https://teakleap-round1.onrender.com](https://teakleap-round1.onrender.com)

---

## Features

- **Domain-Driven Design**: The codebase is split into routes, schemas, services, and repositories for easier maintainability.
- **Async Database Connection**: Uses Motor (`AsyncIOMotorClient`) for non-blocking operations against MongoDB Atlas.
- **Bulk Insert Support**: The `POST` endpoint handles both single JSON objects and arrays of candidates efficiently.
- **Input Validation**: Uses Pydantic to ensure incoming requests have proper structures, valid emails, and correct enum values.
- **Data Integrity**: Checks the database and the active payload for duplicate emails and returns an `HTTP 409 Conflict`.
- **Global Error Handling**: Standardized exception routing to abstract stack traces into clean JSON HTTP responses.
- **Unit Testing**: 100% endpoint test coverage mapped against `mongomock_motor` inside pytest for offline local CI/CD pipelines.

---

## Technology Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** MongoDB Atlas
- **Driver:** Motor
- **Testing:** Pytest, HTTPX, mongomock-motor
- **Web Server:** Uvicorn

---

## API Endpoints

You can explore the live interactive documentation (Swagger) at `/docs` when the server is running.

### 1. Register Candidates (`POST /candidates`)
Accepts a single candidate or an array of candidates.
- **Payload Example**:
```json
[
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "skill": "Python",
    "status": "applied"
  }
]
```
- **Responses:** `201 Created` on success, `409 Conflict` if duplicate email provided.

### 2. List Candidates (`GET /candidates`)
Returns a list of all candidates.
- **Optional Query Params**: `?status=interview` (filters results).
- **Responses:** `200 OK`.

### 3. Update Status (`PUT /candidates/{id}/status`)
Updates the recruitment status for a given candidate by ID.
- **Payload Example**:
```json
{
  "status": "interview"
}
```
*(Valid statuses: `applied`, `interview`, `selected`, `rejected`)*
- **Responses:** `200 OK`, or `404 Not Found`.

---

## Local Development Setup

**1. Clone the repository**
```bash
git clone https://github.com/upadhyayravi023/Teakleap_Round1.git
cd Teakleap_Round1
```

**2. Configure Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows run: .\venv\Scripts\activate
pip install -r requirements.txt
```

**3. Set MongoDB Credentials**
Create a `.env` file in the root directory:
```env
MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DB_NAME="Candidate_Management"
```

**4. Start the Application**
```bash
uvicorn app.main:app --reload --env-file .env
```
The API Swagger documentation will be available locally at `http://127.0.0.1:8000/docs`.

---

## Testing

Run the included test suite locally without an active database connection:
```bash
python -m pytest tests/test_candidates.py -v
```
