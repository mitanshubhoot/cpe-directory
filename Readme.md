# CPE Directory

A full-stack web app for browsing Common Platform Enumeration (CPE) entries using a fast RESTful API and a modern React frontend.

---

## 📌 Features

- Parses and stores data from the official CPE XML dictionary
- REST API built with Flask + SQLite
- Responsive React frontend (with pagination, filtering, search, tooltips)
- Lazy-loaded `cpe.db` from GitHub Releases to support publishing
- Supports deployment on [Render](https://render.com)

---

## 📁 Project Structure

```
cpe-directory/
├── backend/               # Flask + SQLite API
│   ├── api.py             # Main API server
│   ├── db.py              # DB connection helpers
│   ├── parser.py          # Parses official XML and populates DB
│   ├── cpe.db             # (Ignored) DB auto-downloaded from GitHub Release
│   ├── frontend_build     # Static UI (Built from frontend/)
│   └── render.yaml        # Render deploy config
├── frontend/              # React app (optional in dev mode)
│   └── build/             # Copied into backend/frontend_build for deployment
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/mitanshubhoot/cpe-directory.git
cd cpe-directory/backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧠 How It Works

- On app startup, `api.py` checks if `cpe.db` exists.
- If not, it **downloads it from a GitHub Release**:
  ```
  https://github.com/mitanshubhoot/cpe-directory/releases/download/v1.0.0/cpe.db
  ```

You do **not** need to store `cpe.db` or `official-cpe-dictionary_v2.3.xml` in GitHub.

---

## 🧪 Local Development

### Backend

```bash
cd backend
flask run  # or python api.py
```

### Frontend (optional if running separately)

```bash
cd frontend
npm install
npm start
```

To serve frontend from Flask, build and copy it:

```bash
npm run build
cp -r build ../backend/frontend_build
```

---

## ✅ API Endpoints

| Endpoint              | Method | Description                         |
|-----------------------|--------|-------------------------------------|
| `/api/cpes`           | GET    | Paginated list of all entries       |
| `/api/cpes/search`    | GET    | Search by title, URI, deprecation   |

---

## 📂 Ignored Files

These are ignored via `.gitignore` (not stored in repo):

- `cpe.db` – large SQLite DB
- `official-cpe-dictionary_v2.3.xml` – 600MB XML source

Uploaded to GitHub Releases for reprocessing.

---

## 👨‍💻 Author

**Mitanshu Bhoot**  
Indiana University Bloomington  
📧 [mbhoot@iu.edu](mailto:mbhoot@iu.edu)  
🌐 [Portfolio](https://mitanshubhoot.onrender.com)

---

## 📄 License

MIT License © 2025 Mitanshu Bhoot
