# Candidate Management API

A robust, feature-driven recruitment backend architected to manage candidates securely and efficiently. Built entirely using modern Python **FastAPI**, **Pydantic V2**, and **MongoDB Atlas** (via asynchronous `motor`).

### 🌍 **Live Deployment**
> **https://teakleap-round1.onrender.com**

---

## ✨ Features
* **Feature-Driven Architecture**: Modularized domain routing strictly separating API schemas, configurations, data repositories, and orchestrating services.
* **Asynchronous NoSQL Persistence**: Fully integrated asynchronous bindings mapped to a **MongoDB Atlas Cluster** permitting rapid scaling and low-latency `BSON` queries without blocking standard event loops.
* **Automatic Data Validation**: Exhaustive input and output filtering utilizing strictly typed **Pydantic Model Schemas** natively validating emails (`RFC 5322`) alongside bounded Enums restricting Candidate status updates smoothly.
* **Guaranteed Data Integrity**: Proactive conflict validation blocking Duplicate Email addresses, gracefully serving automated `HTTP 409 Conflict` responses.
* **Centralized Exception Handlers**: Hardened security protocols guaranteeing all standard ORM crashes natively reroute avoiding internal stack trace leakage over endpoints.
* **100% Test Coverage**: Complete Pytest suite asserting dynamic API simulations over asynchronous native mock clusters seamlessly without touching real databases.

---

## 🏗️ Technology Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** MongoDB Atlas (Document Database)
* **ORM / Driver:** Motor (AsyncIOMotorClient)
* **Testing:** Pytest, HTTPX, mongomock-motor
* **Server:** Uvicorn

---

## 📖 API Endpoints Definition

Easily test endpoints with automatic interactive documentation available natively at `/docs` (Swagger UI).

### 1. Register a Candidate
* **Route**: `POST /candidates`
* **Response**: `201 Created` / `409 Conflict` (Duplicate Email)
* **Payload**:
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "skill": "Python Backend",
  "status": "applied"
}
```

### 2. View All Candidates
* **Route**: `GET /candidates`
* **Optional Query**: `?status=interview` (Filters dynamically based on Enum selections)
* **Response**: `200 OK`

### 3. Advance Candidate Status
* **Route**: `PUT /candidates/{id}/status`
* **Response**: `200 OK` / `404 Not Found`
* **Payload**:
```json
{
  "status": "interview"
}
```
*(Valid bounds: `applied`, `interview`, `selected`, `rejected`)*

---

## 💻 Local Development Setup

To experiment with this feature architecture on your local desktop:

**1. Clone the repository**
```bash
git clone https://github.com/upadhyayravi023/Teakleap_Round1.git
cd Teakleap_Round1
```

**2. Configure Virtual Environment & Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

**3. Setup Database Credentials**
Create a `.env` file securely inside your project root and paste your exact Atlas Cluster variables:
```env
MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DB_NAME="Candidate_Management"
```

**4. Spin up the ASGI Server**
```bash
uvicorn app.main:app --reload --env-file .env
```
_Visit `http://127.0.0.1:8000/docs` to interface with the endpoints instantly!_

---

## 🧪 Testing Environment

Run the preconfigured test suite to benchmark logic completely offline:
```bash
python -m pytest tests/test_candidates.py -v
```
*(This framework actively leverages `mongomock_motor` intelligently caching transactions locally in RAM to guarantee robust CI/CD execution without any external database internet demands).*
