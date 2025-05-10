# CPE Directory

A full-stack web app for browsing Common Platform Enumeration (CPE) entries using a fast RESTful API and a modern React frontend.

Demo : 
```bash
https://drive.google.com/file/d/1trJq7Ge7NTVgwrcZIIEQcE9NFJV012bm/view?usp=sharing
```


---

## 📌 Features

- Parses and stores data from the official CPE XML dictionary
- REST API built with Flask + SQLite
- Responsive React frontend (pagination, filtering, tooltips, date filters)
- Fully Dockerized for easy deployment

---

## 📁 Project Structure

```
cpe-directory/
├── backend/               # Flask + SQLite API
│   ├── api.py             # Main API server
│   ├── db.py              # DB connection helpers
│   ├── parser.py          # Parses official XML and populates DB
│   ├── cpe.db             # (Ignored) Preprocessed SQLite DB (not tracked)
│   └── frontend_build     # Static React build copied here for deployment
├── frontend/              # React app source (optional in dev mode)
│   └── build/             # Compiled static files
├── Dockerfile             # Docker config
├── .dockerignore          # Docker context cleanup
└── README.md
```

---

# Running the App -
## Step 1)  🧩 Download the db file

This project uses a pre-built SQLite database (`cpe.db`) which is **not included in the repo** because of its size (~360MB).

#### ▶️ Use this link to download it:

```bash
https://github.com/mitanshubhoot/cpe-directory/releases/download/v1.0.0/cpe.db
```
and place it in `backend/`

#### ▶️ Or Optionally, if you'd like to regenerate it yourself:

1: Download the XML file

Get the official CPE dictionary (~650MB) from:

[🔗 NVD CPE Dictionary](https://nvd.nist.gov/products/cpe)

Or directly:

```bash
wget https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml
```

Place the file inside the `backend/` folder.

---

2: Parse and create the database

From inside `backend/`:

```bash
python parser.py
```

This reads the XML and generates `cpe.db`, which can then be used by the API.

---

## Step 2) 🐳 Docker Usage

This app is fully Dockerized and includes the database (`cpe.db`) and frontend assets inside the image.

### 🔧 Build the Docker image

```bash
docker build -t cpe-directory .
```

### ▶️ Run the container locally

```bash
docker run -p 5050:5000 cpe-directory
```

Then visit: [http://localhost:5050](http://localhost:5050)
---

## 🧠 How It Works

- Flask serves a RESTful API and hosts the static React frontend.
- The SQLite database is queried using pagination and filters.
- The React UI shows CPE entries with support for:
  - Truncated columns
  - Link tooltips and popovers
  - Per-column filtering
  - Deprecation date filters
  - Pagination and sorting

---

## ✅ API Endpoints

| Endpoint              | Method | Description                         |
|-----------------------|--------|-------------------------------------|
| `/api/cpes`           | GET    | Paginated list of all entries       |
| `/api/cpes/search`    | GET    | Search by title, URI, deprecation   |

---

## 📂 Ignored Files

These are ignored via `.gitignore` and not pushed to GitHub:

- `backend/cpe.db` – SQLite DB (~360MB)
- `backend/official-cpe-dictionary_v2.3.xml` – Source XML (~650MB)

---

## 👨‍💻 Author

**Mitanshu Bhoot**  
Indiana University Bloomington  
📧 [mbhoot@iu.edu](mailto:mbhoot@iu.edu)  
🌐 [Portfolio](https://mitanshubhoot.onrender.com)

---

## 📄 License

MIT License © 2025 Mitanshu Bhoot
